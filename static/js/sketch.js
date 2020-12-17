var video = document.getElementById('video');
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');

// The detected positions will be inside an array
let poses = [];

// Create a webcam capture
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
    video.srcObject=stream;
    video.play();
  });
}

// A function to draw the video and poses into the canvas.
// This function is independent of the result of posenet
// This way the video will not seem slow if poseNet
// is not detecting a position
function drawCameraIntoCanvas() {
  // Draw the video element into the canvas
  ctx.drawImage(video, 0, 0, 640, 480);
  // We can call both functions to draw all keypoints and the skeletons
  drawKeypoints();
  drawSkeleton();
  window.requestAnimationFrame(drawCameraIntoCanvas);
}
// Loop over the drawCameraIntoCanvas function
drawCameraIntoCanvas();

// Create a new poseNet method with a single detection
const poseNet = ml5.poseNet(video, modelReady);
poseNet.on('pose', gotPoses);

// A function that gets called every time there's an update from the model
function gotPoses(results) {
  poses = results;
  send_pose(poses);
}

function modelReady() {
  console.log("model ready")
  poseNet.multiPose(video)
}

// A function to draw ellipses over the detected keypoints
function drawKeypoints()  {
  // Loop through all the poses detected
  for (let i = 0; i < poses.length; i++) {
    // For each pose detected, loop through all the keypoints
    for (let j = 0; j < poses[i].pose.keypoints.length; j++) {
      let keypoint = poses[i].pose.keypoints[j];
      // Only draw an ellipse is the pose probability is bigger than 0.2
      if (keypoint.score > 0.2) {
        ctx.beginPath();
        ctx.arc(keypoint.position.x, keypoint.position.y, 10, 0, 2 * Math.PI);
        ctx.strokeStyle = 'blue';
        ctx.stroke();
      }
    }
  }
}

// A function to draw the skeletons
function drawSkeleton() {
  // Loop through all the skeletons detected
  for (let i = 0; i < poses.length; i++) {
    // For every skeleton, loop through all body connections
    for (let j = 0; j < poses[i].skeleton.length; j++) {
      let partA = poses[i].skeleton[j][0];
      let partB = poses[i].skeleton[j][1];
      ctx.beginPath();
      ctx.moveTo(partA.position.x, partA.position.y);
      ctx.lineTo(partB.position.x, partB.position.y);
      ctx.strokeStyle = 'blue';
      ctx.stroke();
    }
  }
}

function send_pose(poses){
// Loop through all the poses detected
  for (let i = 0; i < poses.length; i++) {
    var p = {};
    p['score'] = poses[i].pose.score;
    p['keypoints'] = poses[i].pose.keypoints;
    $.ajax(
        {
            type:'POST',
            contentType:'application/json;charset-utf-08',
            dataType:'json',
            url:'http://127.0.0.1:5000/pass_val?value='+JSON.stringify(p),
            success:function (data) {
                var reply=data.reply;
                if (reply=="success")
                {
                    return;
                }
                else
                    {
                    alert("some error occurred in session agent")
                    }
            }
        }
    );
  }
}

// TODO: metodo get per prendere la posa 2D corretta con il post processing e disegnala. Da implementare lato server.
function get_pose(poses){
    $.ajax(
        {
            type:'GET',
            contentType:'application/json;charset-utf-08',
            dataType:'json',
            url:'http://127.0.0.1:5000/get_val',
            success:function (data) {
                var reply=data.reply;
                if (reply!="success" && reply!=null)
                {
                    return data.reply;
                }
                else
                    {
                    alert("some error occurred in session agent")
                    }

            }
        }
    );
}