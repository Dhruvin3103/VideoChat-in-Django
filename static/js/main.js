console.log("hello")

var usernameinput = document.querySelector("#username");
var btnjoin = document.querySelector("#btn-join");
console.log(btnjoin)

var username;
var mapPeers = {};
var webSocket;

function webSocketOnmessage(event){
    
    // console.log(event)
    var parsedData = JSON.parse(event.data);
    var peerUsername = parsedData['peer'];
    var action = parsedData['action']
    console.log(action)
    // this below should be handled in backend
    if(username==peerUsername){
        return;
    }

    var receiver_channel_name = parsedData['message']['receiver_channel_name'];

    if(action == 'new-peer'){
        createOfferer(peerUsername, receiver_channel_name);
        return;
    }

    if(action == 'new-offer'){
        var offer =parsedData['message']['sdp'];

        createAnswer(offer,peerUsername,receiver_channel_name)

        return;
    }

    if(action == 'new-answer'){
        var answer  = parsedData['message']['sdp'];
        var peer = mapPeers[peerUsername][0];

        peer.setRemoteDescription(answer);



 }

    console.log("mess : "+message)
}

btnjoin.addEventListener('click', ()=>{
    username = usernameinput.value;
    console.log(username);
    
    if(username==''){
        return ;
    }

    usernameinput.value = '';
    usernameinput.disabled = true;
    usernameinput.style.visibility = 'hidden';

    btnjoin.disabled = true;
    btnjoin.style.visibility = 'hidden';


    var labelusername = document.querySelector('#label-username');
    labelusername.innerHTML= username; 

    var loc = window.location;
    var wsstart = 'ws://';


    if (loc.protocol == 'https'){
        wsstart = 'wss://';
    }

    var endpoint = wsstart + loc.host + loc.pathname;

    console.log("url : "+endpoint);

    webSocket = new WebSocket(endpoint); 

    webSocket.addEventListener('open', (e)=>{
        console.log("Connection opend");
        sendSignal('new-peer', {});
    });

    webSocket.addEventListener('message', webSocketOnmessage);

    webSocket.addEventListener('close', (e)=>{
        console.log("Connection Closed");
    });

    webSocket.addEventListener('error', (e)=>{
        console.log("Error Occured");
    });

})


var localStream = new MediaStream();

const constraints = {
    'audio':true,
    'video' :true
}

const localVideo = document.querySelector('#local-video')

const btnToggleAudio = document.querySelector('#btn-toggle-audio')
const btnTogglevideo = document.querySelector('#btn-toggle-video')

var userMedia = navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
        localStream = stream;
        localVideo.srcObject = localStream;
        localVideo.muted = true;

        var audioTracks = stream.getAudioTracks()
        var videoTracks = stream.getVideoTracks()

        audioTracks[0].enabled = true;
        videoTracks[0].enabled= true;

        btnToggleAudio.addEventListener('click',()=>{
            audioTracks[0].enabled = !audioTracks[0].enabled;

            if(audioTracks[0].enabled){
                btnToggleAudio.innerHTML = 'Audio mute';
                return;
            }
            btnToggleAudio.innerHTML = 'Audio unmute';

        })

        btnTogglevideo.addEventListener('click',()=>{
            videoTracks[0].enabled = !videoTracks[0].enabled;

            if(videoTracks[0].enabled){
                btnTogglevideo.innerHTML = 'video mute';
                return;
            }
            btnTogglevideo.innerHTML = 'video unmute';

        })
    })
    .catch(error => {
        console.log("Error : "+error);
    })


function sendSignal(action, message){
    var jsonStr = JSON.stringify({
        'peer': username,
        'action': action,
        'message':message,
    })

    webSocket.send(jsonStr);
}

function createOfferer(peerUsername,receiver_channel_name){
    var peer = new RTCPeerConnection(null);

    addLocalTracks(peer);
    var dc = peer.createDataChannel('channel');
    dc.addEventListener('open', ()=>{
        console.log("openned");
    });
    dc.addEventListener('message',dcOnMessage);

    var remoteVideo = createVideo(peerUsername);
    setOnTrack(peer,remoteVideo);


    mapPeers[peerUsername] = [peer, peer.dc];
    peer.addEventListener('iceconnectionstatechange', ()=>{
        var iceConnectionState = peer.iceConnectionState;

        if (iceConnectionState==='failed' || iceConnectionState==='disconnected' || iceConnectionState==='closed'){
            delete mapPeers[peerUsername]; 
            if(iceConnectionState!='closed'){
                peer.close();
            }
            removeVideo(remoteVideo); 
        }
    })

    peer.addEventListener('icecandidate', (event)=>{
        if(event.candidate){
            // console.log('New',JSON.stringify(peer.localDescription));
            return;
        }


        sendSignal('new-offer',{
            'sdp':peer.localDescription,
            'receiver_channel_name':receiver_channel_name 
        })
    })

    peer.createOffer()
        .then(e=>peer.setLocalDescription(e))
        .then(()=>{
            console.log('local descr set successfully');
        })
}

function createAnswer(offer,peerUsername,receiver_channel_name) {
    var peer = new RTCPeerConnection(null);

    addLocalTracks(peer);

    var remoteVideo = createVideo(peerUsername);
    setOnTrack(peer,remoteVideo);

    peer.addEventListener('datachannel', e=>{
        peer.dc=e.channel;
        peer.dc.addEventListener('open', ()=>{
            console.log("openned");
        });
        peer.dc.addEventListener('message',dcOnMessage);

        mapPeers[peerUsername] = [peer, peer.dc]
    })
    
    mapPeers[peerUsername] = [peer, peer.dc];
    peer.addEventListener('iceconnectionstatechange', ()=>{
        var iceConnectionState = peer.iceConnectionState;

        if (iceConnectionState==='failed' || iceConnectionState==='disconnected' || iceConnectionState==='closed'){
            delete mapPeers[peerUsername]; 
            if(iceConnectionState!='closed'){
                peer.close();
            }
            removeVideo(remoteVideo); 
        }
    })

    peer.addEventListener('icecandidate', (event)=>{
        if(event.candidate){
            // console.log('New',JSON.stringify(peer.localDescription));
            return;
        }


        sendSignal('new-answer',{
            'sdp':peer.localDescription,
            'receiver_channel_name':receiver_channel_name
        })
    })

    peer.setRemoteDescription(offer)
        .then(()=>{
            console.log('remote descr is sett for %s .',peerUsername)

            peer.createAnswer();
        })
        .then(a=>{
            console.log('Answer Created !!')

            peer.setLocalDescription(a);
        })
}

function removeVideo(video){
    var videowrapper = video.parentNode;

    videowrapper.parentNode.removeChild(videowrapper);
}

var messageList = document.querySelector("#mess-list");

function createVideo(peerUsername){
    var videoContainer = document.querySelector('#video-container');

    var remoteVideo = document.createElement('video')
    remoteVideo.id = peerUsername+'-video';
    remoteVideo.autoplay=true;
    remoteVideo.playsInline=true;

    var videowrapper = document.createElement('div')

    videoContainer.appendChild(videowrapper)
    videowrapper.appendChild(remoteVideo)

    return remoteVideo;
}

function setOnTrack(peer,remoteVideo){
    var remoteStream = new MediaStream();

    remoteVideo.srcObject = remoteStream
    
    peer.addEventListener('track', async (event)=>{
        remoteStream.addTrack(event.track, remoteStream);   
    })
}


function dcOnMessage(event){
    console.log(event );
    var mess = event.data;
    var li = document.createElement('li');
    li.appendChild(document.createTextNode(mess));
    messageList.appendChild(li);
}

function addLocalTracks(peer){
    localStream.getTracks().forEach(track=>{
        peer.addTrack(track, localStream);
    });

    return ;
}