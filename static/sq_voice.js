/* ═══════════════════════════════════════════════════════════════════════════
   SmartQueue Hospital — Voice + Theme + Feedback + Translation Module
   sq_voice.js  v2.0 — Loaded globally from base.html
   FIXES: theme toggle, voice stop, tap-to-stop, welcome voice, voice optional
   ═══════════════════════════════════════════════════════════════════════════ */

'use strict';

/* ─────────────────────────────────────────────────────────────────────────────
   1. LANGUAGE CODE MAP
   ───────────────────────────────────────────────────────────────────────────── */
var SQ_LANG_VOICE = {
  'en': 'en-IN',
  'hi': 'hi-IN',
  'fr': 'fr-FR',
  'es': 'es-ES',
  'de': 'de-DE',
  'ar': 'ar-SA',
  'bn': 'bn-IN',
  'mr': 'mr-IN',
  'gu': 'gu-IN',
  'ur': 'ur-PK',
};

/* ─────────────────────────────────────────────────────────────────────────────
   2. VOICE ENABLED STATE — load from localStorage immediately
   ───────────────────────────────────────────────────────────────────────────── */
var SQ_VOICE_ENABLED = (localStorage.getItem('sq_voice') !== 'off');

/* ─────────────────────────────────────────────────────────────────────────────
   3. CORE VOICE FUNCTIONS
   ───────────────────────────────────────────────────────────────────────────── */

function stopSpeech() {
  if (window.speechSynthesis) window.speechSynthesis.cancel();
}

/* Alias for backward compat */
function stopSpeaking() { stopSpeech(); }

function speak(text) {
  if (!SQ_VOICE_ENABLED) return;
  if (!window.speechSynthesis) return;

  var clean = String(text || '')
    .replace(/<[^>]*>/g, ' ')
    .replace(/\*\*/g, '').replace(/\*/g, '')
    .replace(/[•#]/g, '').replace(/\s+/g, ' ').trim();
  if (!clean) return;

  const speech = new SpeechSynthesisUtterance(clean);
  speech.lang = "en-IN";
  speech.volume = 1;
  speech.rate = 0.95;
  speech.pitch = 1;

  // ALWAYS cancel before speaking — prevents overlap
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(speech);
}

function _sqLang() {
  var l = document.documentElement.lang || 'en';
  return l.split('-')[0];
}

/* ─────────────────────────────────────────────────────────────────────────────
   4. THEME SYSTEM — fixed light/dark, persisted, default=light
   ───────────────────────────────────────────────────────────────────────────── */

function applyTheme(theme) {
  var t = (theme === 'dark') ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', t);
  localStorage.setItem('sq_theme', t);

  var btn = document.getElementById('themeBtn');
  if (btn) btn.textContent = (t === 'dark') ? '☀️ Light' : '🌙 Dark';

  var ts = document.getElementById('sq-theme-toggle-s');
  if (ts) ts.checked = (t === 'dark');
}

function toggleTheme() {
  var cur = document.documentElement.getAttribute('data-theme') || 'light';
  applyTheme(cur === 'dark' ? 'light' : 'dark');
}

/* Apply saved theme immediately to avoid flash */
(function(){
  var saved = localStorage.getItem('sq_theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
})();

/* ─────────────────────────────────────────────────────────────────────────────
   5. VOICE TOGGLE (settings panel)
   ───────────────────────────────────────────────────────────────────────────── */
function sqToggleVoice(checkbox) {
  SQ_VOICE_ENABLED = checkbox.checked;
  localStorage.setItem('sq_voice', SQ_VOICE_ENABLED ? 'on' : 'off');
  if (SQ_VOICE_ENABLED) {
    setTimeout(function(){ speak('Voice assistant enabled.', _sqLang()); }, 100);
  } else {
    stopSpeech();
  }
}

/* ─────────────────────────────────────────────────────────────────────────────
   6. VOICE INPUT — SpeechRecognition wrapper
   ───────────────────────────────────────────────────────────────────────────── */
var _sqRecognizing = false;
var _sqRecognition = null;

function sqStartListening(onResult, onError, langCode) {
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { if (onError) onError('Voice input not supported.'); return; }

  if (_sqRecognition && _sqRecognizing) { _sqRecognition.stop(); return; }

  _sqRecognition = new SR();
  _sqRecognition.lang = SQ_LANG_VOICE[langCode || _sqLang()] || 'en-IN';
  _sqRecognition.continuous = false;
  _sqRecognition.interimResults = false;
  _sqRecognition.maxAlternatives = 1;

  _sqRecognition.onstart  = function(){ _sqRecognizing = true; };
  _sqRecognition.onend    = function(){ _sqRecognizing = false; };
  _sqRecognition.onresult = function(event){
    var transcript = event.results[0][0].transcript;
    if (onResult) onResult(transcript);
  };
  _sqRecognition.onerror  = function(event){
    _sqRecognizing = false;
    if (onError) onError(event.error);
  };
  _sqRecognition.start();
}

function sqStopListening() {
  if (_sqRecognition && _sqRecognizing) _sqRecognition.stop();
}

/* ─────────────────────────────────────────────────────────────────────────────
   7. MIC BUTTON FACTORY
   ───────────────────────────────────────────────────────────────────────────── */
function sqMicBtn(inputEl, onFinal) {
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'btn-mic';
  btn.title = 'Speak (Voice Input)';
  btn.innerHTML = '🎤';
  btn.setAttribute('aria-label', 'Voice Input');

  btn.addEventListener('click', function(){
    if (_sqRecognizing){
      sqStopListening();
      btn.classList.remove('listening');
      btn.innerHTML = '🎤';
      return;
    }
    btn.classList.add('listening');
    btn.innerHTML = '🔴';
    sqStartListening(
      function(text){ btn.classList.remove('listening'); btn.innerHTML='🎤'; if(inputEl) inputEl.value=text; if(onFinal) onFinal(text); },
      function(err){  btn.classList.remove('listening'); btn.innerHTML='🎤'; console.warn('SQ Voice error:', err); },
      _sqLang()
    );
  });
  return btn;
}

/* ─────────────────────────────────────────────────────────────────────────────
   8. FEEDBACK SYSTEM
   ───────────────────────────────────────────────────────────────────────────── */
function sqSubmitFeedback(rating, comment, source) {
  fetch('/api/feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ rating: rating||0, comment: comment||'', source: source||'settings' })
  }).then(function(r){ return r.json(); })
    .then(function(d){ console.log('Feedback submitted:', d); })
    .catch(function(e){ console.warn('Feedback error:', e); });
}

/* ─────────────────────────────────────────────────────────────────────────────
   9. SETTINGS PANEL TOGGLE
   ───────────────────────────────────────────────────────────────────────────── */
function sqOpenSettings() {
  var p = document.getElementById('sq-settings-panel');
  if (!p) return;
  p.classList.toggle('open');
  if (p.classList.contains('open')) {
    setTimeout(function(){
      document.addEventListener('click', function _close(e){
        if (!p.contains(e.target) && e.target.id !== 'sq-settings-btn'){
          p.classList.remove('open');
          document.removeEventListener('click', _close);
        }
      });
    }, 50);
  }
}

/* ─────────────────────────────────────────────────────────────────────────────
   10. FLOATING STOP VOICE BUTTON — visible when speech is active
   ───────────────────────────────────────────────────────────────────────────── */
function _initStopVoiceButton() {
  if (document.getElementById('sq-stop-voice-btn')) return;

  var btn = document.createElement('button');
  btn.id = 'sq-stop-voice-btn';
  btn.innerHTML = '🔇 Stop Voice';
  btn.title = 'Stop speaking';
  btn.setAttribute('aria-label', 'Stop voice');

  btn.addEventListener('click', function(e){
    e.stopPropagation();
    stopSpeech();
  });

  document.body.appendChild(btn);

  // Poll: show/hide based on speaking state
  setInterval(function(){
    if (!window.speechSynthesis) return;
    var b = document.getElementById('sq-stop-voice-btn');
    if (b) b.classList.toggle('visible', window.speechSynthesis.speaking);
  }, 350);
}

/* ─────────────────────────────────────────────────────────────────────────────
   11. TAP ANYWHERE TO STOP VOICE
   ───────────────────────────────────────────────────────────────────────────── */
function _initTapToStop() {
  document.addEventListener('click', function(e){
    if (!window.speechSynthesis || !window.speechSynthesis.speaking) return;
    var cls = (e.target.className || '').toString();
    // Don't intercept speak/mic/stop buttons
    if (cls.indexOf('msg-speak') > -1) return;
    if (cls.indexOf('btn-mic') > -1) return;
    if (cls.indexOf('token-voice-btn') > -1) return;
    if (e.target.id === 'sq-stop-voice-btn') return;
    stopSpeech();
  }, { passive: true });
}

/* ─────────────────────────────────────────────────────────────────────────────
   12. AUTO-INIT
   ───────────────────────────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', function(){

  /* 1. Theme + UI sync */
  var savedTheme = localStorage.getItem('sq_theme') || 'light';
  applyTheme(savedTheme);

  /* 2. Welcome voice — ONLY once per login (sessionStorage) */
  if (!sessionStorage.getItem('sq_welcomed') && window.SQ_USER_NAME) {
    sessionStorage.setItem('sq_welcomed', 'true');
    setTimeout(function(){
      speak("Welcome back " + window.SQ_USER_NAME);
    }, 1000);
  }

  /* 3. Settings button toggle */
  var settingsBtn = document.getElementById('sq-settings-btn');
  if (settingsBtn) {
    settingsBtn.addEventListener('click', function(e){
      e.stopPropagation();
      sqOpenSettings();
    });
  }

  /* 4. Voice toggle checkbox */
  var vToggle = document.getElementById('sq-voice-toggle');
  if (vToggle) {
    vToggle.checked = SQ_VOICE_ENABLED;
    vToggle.addEventListener('change', function(){ sqToggleVoice(this); });
  }

  /* 5. Theme toggle switch (in settings) */
  var tToggle = document.getElementById('sq-theme-toggle-s');
  if (tToggle) {
    tToggle.addEventListener('change', function(){ applyTheme(this.checked ? 'dark' : 'light'); });
  }

  /* 6. Stop button + tap-to-stop */
  _initStopVoiceButton();
  _initTapToStop();

  /* 7. Star rating */
  document.querySelectorAll('.sq-star-rating').forEach(function(container){
    var stars = container.querySelectorAll('.sq-star');
    stars.forEach(function(star){
      star.addEventListener('click', function(){
        var val = parseInt(star.getAttribute('data-v'), 10);
        container.setAttribute('data-rating', val);
        stars.forEach(function(s, i){ s.classList.toggle('active', i < val); });
      });
      star.addEventListener('mouseenter', function(){
        var val = parseInt(star.getAttribute('data-v'), 10);
        stars.forEach(function(s, i){ s.classList.toggle('hover', i < val); });
      });
    });
    container.addEventListener('mouseleave', function(){
      stars.forEach(function(s){ s.classList.remove('hover'); });
    });
  });

  /* 8. Settings feedback form */
  var settingsFbForm = document.getElementById('sq-settings-feedback-form');
  if (settingsFbForm) {
    settingsFbForm.addEventListener('submit', function(e){
      e.preventDefault();
      var starsEl = document.getElementById('sq-settings-stars');
      var rating  = parseInt(starsEl ? starsEl.getAttribute('data-rating') : '0', 10) || 0;
      var comment = document.getElementById('sq-settings-comment').value.trim();
      sqSubmitFeedback(rating, comment, 'settings');
      document.getElementById('sq-settings-comment').value = '';
      if (starsEl){
        starsEl.setAttribute('data-rating','0');
        starsEl.querySelectorAll('.sq-star').forEach(function(s){ s.classList.remove('active'); });
      }
      var msg = document.getElementById('sq-feedback-sent');
      if (msg){ msg.style.display='block'; setTimeout(function(){ msg.style.display='none'; }, 2500); }
    });
  }

  /* 9. Mic button for chat input */
  var chatInp = document.getElementById('inp');
  if (chatInp && !chatInp.parentNode.querySelector('.btn-mic')) {
    var micBtn = sqMicBtn(chatInp, function(text){
      if (window.send){ chatInp.value = text; window.send(); }
    });
    chatInp.parentNode.insertBefore(micBtn, chatInp.nextSibling);
  }

  /* 10. Mic button for symptom textarea */
  var symInp = document.getElementById('sym');
  if (symInp){
    var symParent = symInp.parentNode;
    if (!symParent.querySelector('.btn-mic')){
      var symMic = sqMicBtn(symInp, null);
      symMic.style.cssText = 'position:absolute;bottom:8px;right:8px;';
      symParent.style.position = 'relative';
      symParent.appendChild(symMic);
    }
  }

  /* 11. Clear welcome session flag on logout */
  document.querySelectorAll('a[href*="/logout"]').forEach(function(a){
    a.addEventListener('click', function(){
      sessionStorage.removeItem('sq_welcomed');
    });
  });

});
