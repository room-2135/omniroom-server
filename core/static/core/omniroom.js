var commandsMapping = {
    "JOINED_CLIENT": onJoined,
    "UPDATE_CAMERAS": onUpdateRequested,
    "SERVER_ERROR": onServerError,
    "MESSAGE": onMessage,
    "SDP_OFFER": onSDPOffer,
    "ICE_CANDIDATE": onICECandidate,
}

var uuid;

var connections = [];

var socket;
window.addEventListener("load", function(){
    connect();
});
function connect() {
    socket = new WebSocket("ws://" + window.location.host);

    socket.onopen = function(e) {
        console.log("WebSocket connection opened");
        join();
    };

    socket.onclose = function(e) {
        console.log("WebSocket connection closed");
        setTimeout(connect, 2000);
    };

    socket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        console.debug(data);
        try {
            commandsMapping[data.command](data);
        } catch(err) {
            onError(err, data);
        }
    };
}

function onError(err, data) {
    console.error("Client error:");
    console.error(err);
}

function onServerError(data) {
    console.error("Server error:");
    console.error(data.error);
}

function join() {
    socket.send(JSON.stringify({
        "command": "JOIN_CLIENT"
    }));
}

function onJoined(data) {
    const identifier = data.identifier;
    console.log("JOINED: " + identifier);
    initCalls();
}

function onUpdateRequested(data) {
    console.log("CAMERAS UPDATE REQUESTED");
    createCall(data["identifier"]);
}

function onMessage(data) {
    console.log("MESSAGE");
    console.log(data["message"])
}

function onSDPOffer(data) {
    console.log("SDP OFFER from: " + data["identifier"]);
    console.debug("Offer: ")
    console.debug(data["offer"]);
    connections[data["identifier"]].setRemoteDescription(data["offer"]).then(() => {
        if (data["offer"].type != "offer")
            return;
        connections[data["identifier"]].createAnswer().then((desc) => {
            connections[data["identifier"]].setLocalDescription(desc).then(function() {
                sdp = {
                   "command": "SDP_ANSWER",
                    "identifier": data["identifier"],
                    "offer": connections[data["identifier"]].localDescription
                }
                console.debug("Sending SDP answer: ");
                console.debug(connections[data["identifier"]].localDescription);
                socket.send(JSON.stringify(sdp));
            });
        });
    });
}

function onICECandidate(data) {
    var candidate = new RTCIceCandidate(data['ice']);
    connections[data["identifier"]].addIceCandidate(candidate).catch(onError);
}

//===========================STREAM=================================
// Override with your own STUN servers if you want
var rtc_configuration = {iceServers: [{urls: "stun:stun.services.mozilla.com"},
                                      {urls: "stun:stun.l.google.com:19302"}]};

function initCalls() {
    console.log("Initiating calls...");
    const cameras = document.getElementsByClassName("camera");
    for (var i = 0; i < cameras.length; i++) {
        const identifier = cameras[i].getAttribute("identifier");
        createCall(identifier);
    }
}

function createCall(identifier) {
    console.log("Creating RTCPeerConnection");

    connections[identifier] = new RTCPeerConnection(rtc_configuration);
    send_channel = connections[identifier].createDataChannel("label", null);
    send_channel.onopen = handleDataChannelOpen;
    send_channel.onmessage = handleDataChannelMessageReceived;
    send_channel.onerror = handleDataChannelError;
    connections[identifier].ondatachannel = onDataChannel;
    connections[identifier].ontrack = (event) => {
        if (getVideoElement(identifier).srcObject !== event.streams[0]) {
            console.log("Incoming stream");
            var loader = document.querySelector(".camera[identifier='" + identifier + "'] .loader-wrapper");
            loader.parentNode.removeChild(loader);
            getVideoElement(identifier).srcObject = event.streams[0];
        }
    };
    connections[identifier].onicecandidate = (event) => {
        if (event.candidate == null) {
            console.log("ICE Candidate was null, done");
            return;
        }
        socket.send(JSON.stringify({"command": "ICE_ANSWER", "identifier": identifier, "ice": event.candidate}));
    };
    socket.send(JSON.stringify({"command": "CALL", "identifier": identifier}));
}

function getVideoElement(identifier) {
    return document.querySelector(".camera[identifier='" + identifier + "'] .camera__video");
}

// Local description was set, send it to peer
function onLocalDescription(desc) {
    connections[data["identifier"]].setLocalDescription(desc).then(function() {
        socket.send(JSON.stringify({"command": "CLIENT_MSG", "camera": data["identifier"], "sdp": connections[data["identifier"]].localDescription}));
    });
}

const handleDataChannelOpen = (event) => {
    console.log("dataChannel.OnOpen", event);
};

const handleDataChannelMessageReceived = (event) =>{
    console.log("dataChannel.OnMessage:", event, event.data.type);

    setStatus("Received data channel message");
    if (typeof event.data === "string" || event.data instanceof String) {
        console.log("Incoming string message: " + event.data);
        var textarea = document.getElementById("text")
        textarea.value = textarea.value + "\n" + event.data
    } else {
        console.log("Incoming data message");
    }
    send_channel.send("Hi! (from browser)");
};

const handleDataChannelError = (error) =>{
    console.log("dataChannel.OnError:", error);
};

const handleDataChannelClose = (event) =>{
    console.log("dataChannel.OnClose", event);
};

function onDataChannel(event) {
    console.log("Incoming data channel");
    let receiveChannel = event.channel;
    receiveChannel.onopen = handleDataChannelOpen;
    receiveChannel.onmessage = handleDataChannelMessageReceived;
    receiveChannel.onerror = handleDataChannelError;
    receiveChannel.onclose = handleDataChannelClose;
}
