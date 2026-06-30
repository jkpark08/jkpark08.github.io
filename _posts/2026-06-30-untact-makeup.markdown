---
layout: project
title: Untact Makeup
project_title: Untact Makeup
project_subtitle: Reference-Guided Virtual Makeup Transfer
project_label: Interactive Demo
home_section: project
authors: <strong>Joonkyu Park</strong>
date: 2026-06-30 13:32:20 +0900
description: Personal Project
img: untact-makeup/sample.png
summary: A web interface for reference-guided virtual makeup transfer. Upload a portrait and optionally provide separate skin, lip, and eye references.
code_url: https://github.com/jkpark0825/untact_makeup
tags:
  - Virtual Makeup
  - Face Editing
  - Generative Models
  - Interactive Demo
---

## Overview

**Untact Makeup** transfers makeup appearance from one or more reference portraits to a source portrait. The underlying inference code aligns faces with 68-point landmarks, optionally combines separate skin, lip, and eye references, and feeds the prepared source/reference pair to a TensorFlow-v1 makeup-transfer generator.

> **Deployment note.** This page is hosted statically through Jekyll/GitHub Pages, so model inference is served by a separate Python backend. Set the API endpoint below to the deployed backend URL. The deployment package is included with this project update.

---

## Interactive Demo

<div class="untact-demo" id="untact-demo">
  <div class="untact-demo__bar">
    <div>
      <span class="untact-demo__eyebrow">LIVE INFERENCE</span>
      <h3>Apply reference-guided makeup</h3>
    </div>
    <span class="untact-demo__status" id="untact-status">Configure the API endpoint</span>
  </div>

  <div class="untact-demo__endpoint">
    <label for="untact-api">Model API endpoint</label>
    <div class="untact-demo__endpoint-row">
      <input id="untact-api" type="url" placeholder="https://your-server.example/untact-makeup" aria-label="Model API endpoint">
      <button type="button" id="untact-save-api">Save</button>
    </div>
    <p>The backend accepts <code>POST {endpoint}/api/makeup</code>. The endpoint is saved only in this browser.</p>
  </div>

  <form id="untact-form" class="untact-demo__grid">
    <label class="untact-demo__upload untact-demo__upload--source">
      <span class="untact-demo__upload-label">1. Source portrait <em>required</em></span>
      <input id="untact-source" name="source" type="file" accept="image/*" required>
      <img id="untact-source-preview" src="{{ '/assets/img/untact-makeup/sample.png' | relative_url }}" alt="Source portrait preview">
      <span class="untact-demo__hint">Choose a frontal, single-face image.</span>
    </label>

    <div class="untact-demo__references">
      <label class="untact-demo__upload">
        <span class="untact-demo__upload-label">Skin reference <em>optional</em></span>
        <input id="untact-skin" name="skin" type="file" accept="image/*">
        <span class="untact-demo__file-name" data-default="Use source appearance">Use source appearance</span>
      </label>
      <label class="untact-demo__upload">
        <span class="untact-demo__upload-label">Lip reference <em>optional</em></span>
        <input id="untact-lip" name="lip" type="file" accept="image/*">
        <span class="untact-demo__file-name" data-default="Keep source lips">Keep source lips</span>
      </label>
      <label class="untact-demo__upload">
        <span class="untact-demo__upload-label">Eye reference <em>optional</em></span>
        <input id="untact-eye" name="eye" type="file" accept="image/*">
        <span class="untact-demo__file-name" data-default="Keep source eyes">Keep source eyes</span>
      </label>

      <button class="untact-demo__submit" id="untact-submit" type="submit">Apply Makeup</button>
      <p class="untact-demo__privacy">Uploads are sent only to the configured inference server and are discarded after the request completes.</p>
    </div>

    <div class="untact-demo__result">
      <span class="untact-demo__upload-label">2. Result</span>
      <div class="untact-demo__result-frame">
        <img id="untact-result-preview" src="{{ '/assets/img/untact-makeup/result.png' | relative_url }}" alt="Example makeup-transfer result">
      </div>
      <span class="untact-demo__hint" id="untact-result-caption">Repository example. Configure an endpoint and upload an image to run inference.</span>
    </div>
  </form>
</div>

<style>
.untact-demo{margin:2rem 0 3rem;padding:1.4rem;border:1px solid #d9e0ec;border-radius:18px;background:#fbfcff;box-shadow:0 12px 36px rgba(27,45,85,.08);font-family:inherit}.untact-demo *{box-sizing:border-box}.untact-demo__bar{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;margin-bottom:1.15rem}.untact-demo__eyebrow{display:block;color:#5568a8;font-size:.71rem;font-weight:800;letter-spacing:.12em}.untact-demo h3{margin:.2rem 0 0;font-size:1.3rem}.untact-demo__status{display:inline-flex;align-items:center;min-height:30px;padding:.3rem .6rem;border-radius:999px;background:#eff2f8;color:#596579;font-size:.78rem;font-weight:700}.untact-demo__status.is-ready{background:#e5f6ed;color:#187149}.untact-demo__status.is-busy{background:#fff3d7;color:#8b5d00}.untact-demo__status.is-error{background:#ffe8e8;color:#a32a2a}.untact-demo__endpoint{margin-bottom:1.2rem;padding:1rem;border-radius:12px;background:#f1f4fb}.untact-demo__endpoint label,.untact-demo__upload-label{display:block;margin-bottom:.42rem;font-size:.8rem;font-weight:800;color:#26324d}.untact-demo__endpoint-row{display:flex;gap:.55rem}.untact-demo__endpoint input{width:100%;min-width:0;padding:.72rem .8rem;border:1px solid #cbd5e7;border-radius:9px;background:white;font:inherit;font-size:.86rem}.untact-demo button{border:0;border-radius:9px;background:#263b7d;color:white;padding:.68rem .86rem;font:inherit;font-size:.84rem;font-weight:800;cursor:pointer}.untact-demo button:hover{background:#1e306a}.untact-demo__endpoint p,.untact-demo__privacy{margin:.48rem 0 0;color:#68758a;font-size:.76rem;line-height:1.45}.untact-demo__grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,.68fr) minmax(0,1fr);gap:1rem;align-items:start}.untact-demo__upload{display:block}.untact-demo__upload em{font-style:normal;font-weight:600;color:#7f899a}.untact-demo__upload input[type=file]{display:block;width:100%;margin-bottom:.55rem;padding:.4rem;border:1px dashed #b7c4dc;border-radius:8px;background:white;font-size:.76rem}.untact-demo__upload--source>img,.untact-demo__result-frame{width:100%;min-height:234px;border:1px solid #d3dce9;border-radius:12px;background:#edf1f8;overflow:hidden}.untact-demo__upload--source>img{display:block;object-fit:contain;aspect-ratio:1/1}.untact-demo__references{display:flex;flex-direction:column;gap:.62rem;padding:.8rem;border-radius:12px;background:white;border:1px solid #e0e7f1}.untact-demo__file-name{display:block;min-height:1.2rem;color:#6e7b8f;font-size:.74rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.untact-demo__submit{width:100%;margin-top:.25rem;min-height:42px}.untact-demo__submit:disabled{cursor:not-allowed;background:#8b96ae}.untact-demo__result-frame{display:flex;align-items:center;justify-content:center;aspect-ratio:1/1}.untact-demo__result-frame img{width:100%;height:100%;object-fit:contain}.untact-demo__hint{display:block;margin-top:.52rem;color:#68758a;font-size:.76rem;line-height:1.45}@media(max-width:760px){.untact-demo__bar{flex-direction:column}.untact-demo__grid{grid-template-columns:1fr}.untact-demo__endpoint-row{flex-direction:column}.untact-demo__endpoint-row button{width:100%}}
</style>

<script>
(() => {
  const $ = (id) => document.getElementById(id);
  const endpointInput = $('untact-api');
  const status = $('untact-status');
  const form = $('untact-form');
  const submit = $('untact-submit');
  const sourcePreview = $('untact-source-preview');
  const resultPreview = $('untact-result-preview');
  const resultCaption = $('untact-result-caption');
  const storageKey = 'untact_makeup_api_endpoint';
  const placeholder = 'https://your-server.example/untact-makeup';

  endpointInput.value = localStorage.getItem(storageKey) || '';
  const setStatus = (text, type = '') => {
    status.textContent = text;
    status.className = `untact-demo__status ${type}`;
  };
  const endpoint = () => endpointInput.value.trim().replace(/\/$/, '');
  const endpointIsConfigured = () => /^https?:\/\//.test(endpoint()) && !endpoint().includes('your-server.example');

  $('untact-save-api').addEventListener('click', () => {
    if (!endpointIsConfigured()) {
      setStatus('Enter a valid API URL', 'is-error');
      endpointInput.focus();
      return;
    }
    localStorage.setItem(storageKey, endpoint());
    setStatus('API endpoint saved', 'is-ready');
  });

  ['source', 'skin', 'lip', 'eye'].forEach((key) => {
    const input = $(`untact-${key}`);
    input.addEventListener('change', () => {
      const file = input.files && input.files[0];
      const label = input.parentElement.querySelector('.untact-demo__file-name');
      if (label) label.textContent = file ? file.name : label.dataset.default;
      if (key === 'source' && file) sourcePreview.src = URL.createObjectURL(file);
    });
  });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!endpointIsConfigured()) {
      setStatus('Configure the API endpoint first', 'is-error');
      endpointInput.focus();
      return;
    }
    const source = $('untact-source').files[0];
    if (!source) {
      setStatus('Select a source portrait', 'is-error');
      return;
    }

    const payload = new FormData();
    payload.append('source', source);
    ['skin', 'lip', 'eye'].forEach((key) => {
      const file = $(`untact-${key}`).files[0];
      if (file) payload.append(key, file);
    });

    submit.disabled = true;
    submit.textContent = 'Applying Makeup…';
    setStatus('Running inference', 'is-busy');
    resultCaption.textContent = 'The model is processing the source and reference images.';
    try {
      const response = await fetch(`${endpoint()}/api/makeup`, {method: 'POST', body: payload});
      if (!response.ok) {
        let message = `Request failed (${response.status})`;
        try { message = (await response.json()).error || message; } catch (_) {}
        throw new Error(message);
      }
      const image = await response.blob();
      resultPreview.src = URL.createObjectURL(image);
      resultPreview.alt = 'Generated virtual makeup result';
      resultCaption.textContent = 'Generated result from the configured Untact Makeup inference server.';
      setStatus('Inference complete', 'is-ready');
    } catch (error) {
      setStatus(error.message || 'Inference failed', 'is-error');
      resultCaption.textContent = 'The request could not be completed. Check the endpoint, model checkpoint, and server logs.';
    } finally {
      submit.disabled = false;
      submit.textContent = 'Apply Makeup';
    }
  });

  setStatus(endpointIsConfigured() ? 'API endpoint ready' : 'Configure the API endpoint', endpointIsConfigured() ? 'is-ready' : '');
})();
</script>

---

## How It Works

1. The backend detects and aligns the source face using dlib facial landmarks.
2. Optional skin, lip, and eye references are independently aligned and used to construct a reference appearance.
3. The TensorFlow-v1 generator receives the aligned source and reference images and returns the synthesized makeup result.

The interactive page supports one source portrait and independent references for skin, lips, and eyes. Leaving any reference empty preserves the corresponding appearance from the source portrait.

---

## Deployment

The project page is static, while the inference model runs as a separate Flask service. Deploy the included backend on a GPU or CPU server, configure its CORS allowlist for this site, and enter its public URL in the demo above. The original repository must include the TensorFlow checkpoint under `models/`, because the public source tree expects `models/model.meta` and a matching checkpoint during inference.

For standalone use and code details, see the [original implementation](https://github.com/jkpark0825/untact_makeup).
