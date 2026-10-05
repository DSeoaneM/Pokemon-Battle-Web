(function () {
  var LOOP_BEGIN = 14.4;
  var END          = 17.6;
  var RESPALDO_MS  = 4000;

  var video = document.getElementById('intro');
  var box  = document.querySelector('.box');
  var started = false;

  function loopControl() {
    if (video.currentTime >= END - 0.05) video.currentTime = LOOP_BEGIN;
    requestAnimationFrame(loopControl);
  }
  video.addEventListener('play', function () { requestAnimationFrame(loopControl); }, { once: true });
  video.addEventListener('ended', function () { video.currentTime = LOOP_BEGIN; video.play(); });

  function initiate() {
    if (started) return;
    started = true;
    var p = video.play();
    if (p && p.catch) p.catch(function () {});
  }

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    video.addEventListener('loadedmetadata', function () { video.currentTime = LOOP_BEGIN; });
    return;
  }

  box.addEventListener('animationend', function (e) {
    if (e.animationName === 'abrir') initiate();
  });
  setTimeout(initiate, RESPALDO_MS);
})();
