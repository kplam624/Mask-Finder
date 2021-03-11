// The following is from a tutorial from
// https://html5.tutorials24x7.com/blog/how-to-capture-image-from-camera
// This code is to experiment to be used for application.

var data_uri

// The buttons to start & stop stream and to capture the image
var btnStart = document.getElementById( "btn-start" );
var btnStop = document.getElementById( "btn-stop" );
var btnCapture = document.getElementById( "btn-capture" );

// The stream & capture
var stream = document.getElementById( "stream" );
var capture = document.getElementById( "capture" );
var snapshot = document.getElementById( "snapshot" );

// The video stream
var cameraStream = null;

// Attach listeners
btnStart.addEventListener( "click", startStreaming );
btnStop.addEventListener( "click", stopStreaming );
btnCapture.addEventListener( "click", captureSnapshot );

// Start Streaming
function startStreaming() {

  var mediaSupport = 'mediaDevices' in navigator;

  if( mediaSupport && null == cameraStream ) {

    navigator.mediaDevices.getUserMedia( { video: true } )
    .then( function( mediaStream ) {

      cameraStream = mediaStream;

      stream.srcObject = mediaStream;

      stream.play();
    })
    .catch( function( err ) {

      console.log( "Unable to access camera: " + err );
    });
  }
  else {

    alert( 'Your browser does not support media devices.' );

    return;
  }
}

// Stop Streaming
function stopStreaming() {

  if( null != cameraStream ) {

    var track = cameraStream.getTracks()[ 0 ];

    track.stop();
    stream.load();

    cameraStream = null;
  }
}

function captureSnapshot() {

  if( null != cameraStream ) {

    var ctx = capture.getContext( '2d' );
    var img = new Image();

    ctx.drawImage( stream, 0, 0, capture.width, capture.height );
  
    img.src   = capture.toDataURL( "image/jpg" );
    img.width = 240;

    snapshot.innerHTML = '';

    // We would like to save the datauri for a post request.

    snapshot.appendChild( img );

    data_uri = snapshot.firstChild.getAttribute( "src" );
    
    console.log(data_uri);

    // Attempt to upload just the data uri
    // upload(data_uri);

    // Create a blob of the data_uri and to upload it to the server.
    var imageData   = dataURItoBlob( data_uri );
    
    upload(imageData);

    warning();
  }
}

function upload(images){

  var request = new XMLHttpRequest();
  
  request.open("POST","/webcamcapture", true);

  // request.open("POST","http://localhost:5000/webcamcapture", true);

  content = new FormData();

  // Creates a new form to be sent to the server
  content.append("image", images, "saved_image.jpg");

  console.log(content);

  // Attempting to use a different form and sending a data uri instead of an image.
  // content.append("image", images);

  request.send(content);
  
}

// This code will create a blob object.
function dataURItoBlob( dataURI ) {

  // Splits the datauri string.
	var byteString = atob( dataURI.split( ',' )[ 1 ] );
	var mimeString = dataURI.split( ',' )[ 0 ].split( ':' )[ 1 ].split( ';' )[ 0 ];
	
	var buffer	= new ArrayBuffer( byteString.length );
	var data	= new DataView( buffer );
	
	for( var i = 0; i < byteString.length; i++ ) {
	
		data.setUint8( i, byteString.charCodeAt( i ) );
	}
	
	return new Blob( [ buffer ], { type: mimeString } );
}