$(function () {
  var socket = io();
  var streaming = 0;
  var video = $('body > video')[0],
    cvs = document.createElement('canvas'),
    ctx = cvs.getContext('2d');

  navigator.getMedia = (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);

  navigator.getMedia({ video: !0, audio: !1 }, function (stream) {
    if (navigator.mozGetUserMedia)
      video.mozSrcObject = stream;
    else {
      var vu = window.URL || window.webkitURL;
      video.src = vu.createObjectURL(stream);
    }
    video.play();
  }, function (error) {
    if (window.console)
      console.error(error);
  });

  video.addEventListener('canplay', function (ev) {
    if (!streaming) {
      height = video.videoHeight / (video.videoWidth / width);
      video.setAttribute('width', width);
      video.setAttribute('height', height);
      streaming = !0;
    }
  }, !1);

  var takePic = function () {
    console.log("taking picture");
    cvs.width = video.width;
    cvs.height = video.height;

    ctx.drawImage(video, 0, 0, cvs.width, cvs.height);

    var a = $('<a href="' + cvs.toDataURL('image/png') + '" download="photo.png"></a>').appendTo('body');
    a[0].click();
    a.remove();
  }
  $(video).on('click', takePic);

  socket.on('take_picture', takePic);



});