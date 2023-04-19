//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
	console.log("recordButton clicked");

	/*
		Simple constraints object, for more advanced audio features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/
    
    var constraints = { audio: true, video:false }

 	/*
    	Disable the record button until we get a success or fail from getUserMedia() 
	*/

	recordButton.disabled = true;
	stopButton.disabled = false;
	pauseButton.disabled = false

	/*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device

		*/
		audioContext = new AudioContext();

		//update the format 
		document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

		/*  assign to gumStream for later use  */
		gumStream = stream;
		
		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);

		/* 
			Create the Recorder object and configure to record mono sound (1 channel)
			Recording 2 channels  will double the file size
		*/
		rec = new Recorder(input,{numChannels:1})

		//start the recording process
		rec.record()

		console.log("Recording started");

	}).catch(function(err) {
	  	//enable the record button if getUserMedia() fails
    	recordButton.disabled = false;
    	stopButton.disabled = true;
    	pauseButton.disabled = true
	});
}

function pauseRecording(){
	console.log("pauseButton clicked rec.recording=",rec.recording );
	if (rec.recording){
		//pause
		rec.stop();
		pauseButton.innerHTML="Resume";
	}else{
		//resume
		rec.record()
		pauseButton.innerHTML="Pause";

	}
}

function stopRecording() {
	console.log("stopButton clicked");

	//disable the stop button, enable the record to allow for new recordings
	stopButton.disabled = true;
	recordButton.disabled = false;
	pauseButton.disabled = true;

	//reset button just in case the recording is stopped while paused
	pauseButton.innerHTML="Pause";
	
	//tell the recorder to stop the recording
	rec.stop();

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//create the wav blob and pass it on to RecognizeSpeech
	rec.exportWAV(RecognizeSpeech);
}

function RecognizeSpeech(blob) {
	let url = URL.createObjectURL(blob);
	let audioPlayer = document.getElementById("audio-player");
	let inputText = document.getElementById("input_text");
	let inputText_2 = document.getElementById("input_text_2");

	//add controls to the <audio> element
	audioPlayer.controls = true;
	audioPlayer.src = url;

	let xhr=new XMLHttpRequest();
	xhr.onload=function(e) {
	  if(this.readyState === 4) {
		  console.log("Server returned: ",e.target.responseText);
	  }
	};
	let fd=new FormData();
	fd.append("audio_data",blob);
	xhr.open("POST","/process_audio",true);

	xhr.responseType = 'json';
	xhr.send(fd);
	xhr.onload = function() {
		let responseObj = xhr.response;
		let responseText = responseObj.text;
		console.log('后端返回的文本:', responseText);
		 inputText.value = responseText;
		 inputText_2.value = responseText;
	  // alert(responseObj.message);
	};
}


function sendCredentials() {
  // 获取账号和密码输入框的值
  // let download_path = document.getElementById("download_path").value;
  let API_key = document.getElementById("API_key").value;

  // 创建XMLHttpRequest对象
  let xhr = new XMLHttpRequest();

  // 设置请求方式和请求地址
  xhr.open("POST", "/process_info");

  // 设置请求头
  xhr.setRequestHeader("Content-Type", "application/json");

  // 将账号和密码作为JSON数据发送到后端
  // xhr.send(JSON.stringify({ download_path: download_path, API_key: API_key }));
  xhr.send(JSON.stringify({ API_key: API_key }));

  // 监听请求状态变化
  xhr.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
      // 请求成功
      console.log(xhr.responseText);
	  alert("Submission successful！");
    } else if (this.readyState === 4 && this.status !== 200) {
      // 请求失败
      console.error("ERROR");
    }
  };
}


function GetTransText(input="input_text", output="translation_text", reverse=false, model="cone", add_history=false) {
	let li = document.createElement('li');
	let textResult = document.createElement('textResult');
	let TransResult = document.getElementById(output);

  // 获取输入文本框的值
  let inputText = document.getElementById(input).value;

  // 创建XMLHttpRequest对象，发送POST请求到后端
  let xhr = new XMLHttpRequest();
  xhr.open('POST', '/get_translation');
  xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  // 将输入文本作为JSON数据发送到后端
  xhr.send(JSON.stringify({ input_text: inputText, reverse: reverse, model: model}));

  // 监听请求状态变化
  xhr.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
      // 解析JSON响应，将翻译结果显示在页面上
      let response = JSON.parse(xhr.responseText);
	  let responseText = response.text;
	  let responseTrans = response.translation;
      // document.getElementById("output_text").innerHTML = outputText;
		TransResult.value = responseTrans;
		console.log('后端返回的翻译文本:', responseTrans);

		if (add_history) {
			textResult.innerHTML = 'You: ' + document.getElementById("input_text").value +  ' ' + '|' + ' ' + 'Translation: ' + document.getElementById("translation_text").value
				+  ' ' + '|' + ' ' + 'Chatgpt: ' + document.getElementById("chat_text").value  +  ' ' + '|' + ' ' + 'Chat Translation: ' + responseTrans + '<br>';// Hello, world!
		}

    } else if (this.readyState === 4 && this.status !== 200) {
      console.error("请求失败");
    }
  };
  if (add_history) {
  	li.appendChild(textResult);
	recordingsList.appendChild(li);
		}
}


function GetChatgptText(input="input_text_2", output="chat_text_2", add_history=true, translate=false) {
	let li = document.createElement('li');
	let textResult = document.createElement('textResult');
	let ChatResult = document.getElementById(output);

  // 获取输入文本框的值
  let inputText = document.getElementById(input).value;

  // 创建XMLHttpRequest对象，发送POST请求到后端
  let xhr = new XMLHttpRequest();
  xhr.open('POST', '/get_chatgpt');
  xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  // 将输入文本作为JSON数据发送到后端
  xhr.send(JSON.stringify({ input_text: inputText, translate: translate }));

  // 监听请求状态变化
  xhr.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
      // 解析JSON响应，将翻译结果显示在页面上
      let response = JSON.parse(xhr.responseText);
	  let responseText = response.text;
      let responseChattext = response.chat_text;
      // document.getElementById("output_text").innerHTML = outputText;
		ChatResult.value = responseChattext;
		console.log('后端返回的chat文本:', responseChattext);

		if (add_history) {
			if (translate) {
				textResult.innerHTML = 'You: ' + document.getElementById("input_text").value +  ' ' + '|' + ' ' + 'Translation: ' + responseText + ' ' + '|' + ' ' + 'Chatgpt: ' + responseChattext + '<br>';
			}
			else {
				textResult.innerHTML = 'You: ' + responseText + ' ' + '|' + ' ' + 'Chatgpt: ' + responseChattext + '<br>';
			}
		}

    } else if (this.readyState === 4 && this.status !== 200) {
      console.error("请求失败");
    }
  };
    if (add_history) {
		li.appendChild(textResult);
		recordingsList.appendChild(li);
	}
}

