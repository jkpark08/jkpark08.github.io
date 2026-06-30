"""Flask API wrapper for the original Untact Makeup TensorFlow-v1 inference code.

Expected layout:
  deployment/
    app.py
    requirements.txt
    untact_makeup/                # clone of jkpark0825/untact_makeup
      full_makeup.py
      shape_predictor_68_face_landmarks.dat
      models/model.meta
      models/<checkpoint files>

Set UNTACT_MAKEUP_REPO to an alternate clone path when needed.
"""
from __future__ import annotations

import importlib
import io
import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent
REPO_DIR = Path(os.environ.get("UNTACT_MAKEUP_REPO", BASE_DIR / "untact_makeup")).resolve()
ALLOWED_ORIGINS = [x.strip() for x in os.environ.get("ALLOWED_ORIGINS", "*").split(",") if x.strip()]
MAX_UPLOAD_MB = int(os.environ.get("MAX_UPLOAD_MB", "12"))

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGINS}})

_runtime = None
_runtime_error: Optional[str] = None


def _require_model_files() -> None:
    required = [
        REPO_DIR / "full_makeup.py",
        REPO_DIR / "shape_predictor_68_face_landmarks.dat",
        REPO_DIR / "models" / "model.meta",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise RuntimeError(
            "Missing Untact Makeup inference files: " + "; ".join(missing) + ". "
            "The public repository code expects a TensorFlow-v1 model checkpoint under models/."
        )


def _load_runtime():
    """Loads the original model lazily, so /health remains useful before configuration."""
    global _runtime, _runtime_error
    if _runtime is not None:
        return _runtime
    if _runtime_error is not None:
        raise RuntimeError(_runtime_error)

    try:
        _require_model_files()
        # The original scripts use relative model and landmark paths.
        os.chdir(REPO_DIR)
        if str(REPO_DIR) not in sys.path:
            sys.path.insert(0, str(REPO_DIR))
        _runtime = importlib.import_module("full_makeup")
        return _runtime
    except Exception as exc:  # convert initialization failures into an informative HTTP response
        _runtime_error = str(exc)
        raise RuntimeError(_runtime_error) from exc


def _decode_upload(field_name: str, required: bool = False) -> Optional[np.ndarray]:
    file = request.files.get(field_name)
    if file is None or not file.filename:
        if required:
            raise ValueError(f"Missing required image field: {field_name}")
        return None

    raw = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(raw, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"{field_name} is not a readable image")
    return image


def _write_temp_image(image: Optional[np.ndarray], directory: Path, name: str) -> Optional[str]:
    if image is None:
        return None
    path = directory / f"{name}.png"
    if not cv2.imwrite(str(path), image):
        raise RuntimeError(f"Could not write temporary {name} image")
    return str(path)


@app.get("/health")
def health():
    ready = _runtime is not None
    checkpoint_found = (REPO_DIR / "models" / "model.meta").exists()
    return jsonify(
        {
            "status": "ready" if ready else "not_loaded",
            "repository": str(REPO_DIR),
            "checkpoint_found": checkpoint_found,
            "detail": _runtime_error,
        }
    )


@app.post("/api/makeup")
def makeup():
    try:
        source = _decode_upload("source", required=True)
        skin = _decode_upload("skin")
        lip = _decode_upload("lip")
        eye = _decode_upload("eye")
        runtime = _load_runtime()

        with tempfile.TemporaryDirectory(prefix="untact_makeup_") as temp_dir:
            temp_path = Path(temp_dir)
            skin_path = _write_temp_image(skin, temp_path, "skin")
            lip_path = _write_temp_image(lip, temp_path, "lip")
            eye_path = _write_temp_image(eye, temp_path, "eye")

            # full_makeup.py refers to a global `dets` variable but does not initialize it
            # inside full_makeup(). Initialize it from the current source image before inference.
            source_rgb = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
            runtime.dets = runtime.detector(source_rgb, 1)
            if len(runtime.dets) == 0:
                raise ValueError("No face was detected in the source image")

            _, _, output = runtime.full_makeup(
                source,
                skin_image=skin_path,
                lip_image=lip_path,
                eye_image=eye_path,
            )

            ok, encoded = cv2.imencode(".png", output)
            if not ok:
                raise RuntimeError("Could not encode the generated result")
            return send_file(
                io.BytesIO(encoded.tobytes()),
                mimetype="image/png",
                as_attachment=False,
                download_name="untact_makeup_result.png",
            )

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503
    except Exception as exc:  # keep internal tracebacks out of public responses
        app.logger.exception("Untact Makeup inference failed")
        return jsonify({"error": f"Inference failed: {exc}"}), 500


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": f"Upload exceeds the {MAX_UPLOAD_MB} MB limit"}), 413


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))
    app.run(host="0.0.0.0", port=port, debug=False)
