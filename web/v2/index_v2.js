let socket = io();

var leftJoyStick = nipplejs.create({
    zone: document.getElementById('leftJoyStick'),
    mode: 'static',
    position: { left: '50%', top: '50%' },
    color: '#ff5e52'
});

var rightJoyStick = nipplejs.create({
    zone: document.getElementById('rightJoyStick'),
    mode: 'static',
    position: { left: '50%', top: '50%' },
    color: '#02bbde'
});


let leftPrevMessage = '';

leftJoyStick.on('move', function (evt, data) {
    let x = data.vector.x;
    let y = data.vector.y;
    let message = '';

    if (y < -0.5) {
        message += 's'; //뒤
    } else if (y > 0.5) {
        message += 'w'; //앞
    }

    if (x < -0.5) {
        message += 'a'; //왼
    } else if (x > 0.5) {
        message += 'd'; //오
    }

    if (message && message !== leftPrevMessage) {
        leftPrevMessage = '';
        send_arrow('[arrow-stop]');
        send_arrow('[arrow]' + message);
        startVibrate(5);
        leftPrevMessage = message;
    }
});

leftJoyStick.on('end', function (evt, data) {
    if (leftPrevMessage) {
        send_arrow('[arrow-stop]');
        startVibrate(5);
        leftPrevMessage = '';
    }
});

let rightPrevMessage = '';
rightJoyStick.on('move', function (evt, data) {
    let x = data.vector.x;
    let y = data.vector.y;
    let message = '';

    if (y < -0.5) {
        message += 'k'; //뒤
    } else if (y > 0.5) {
        message += 'i'; //앞
    }

    if (x < -0.5) {
        message += 'j'; //왼
    } else if (x > 0.5) {
        message += 'l'; //오
    }

    if (message && message !== rightPrevMessage) {
        rightPrevMessage = '';
        send_arrow('[arrow-stop]');
        send_arrow('[arrow]' + message);
        startVibrate(5);
        rightPrevMessage = message;
    }
});

rightJoyStick.on('end', function (evt, data) {
    if (rightPrevMessage) {
        send_arrow('[arrow-stop]');
        startVibrate(5);
        rightPrevMessage = '';
    }
});

function connectToPC() {

    const defaultServerIP = window.location.hostname;
    const serverIP = prompt(`PC의 IP 주소 입력`, defaultServerIP) || defaultServerIP;
    const serverPort = 8888; // 사용할 포트 번호로 변경

    // WebSocket을 사용하여 PC와 연결
    socket = new WebSocket(`ws://${serverIP}:${serverPort}`);

    // 연결이 열리면 메시지를 보냄
    socket.addEventListener("open", (event) => {
        console.log(`Received from PC: ${event.data}`);
        Toastify({
            text: "연결 성공",
            duration: 1000,
            position: "center",
            style: {
                borderRadius: '20px',
                fontSize: "20px",
            }
        }).showToast();
        startVibrate([5, 50, 50, 300, 10]);
        document.documentElement.webkitRequestFullscreen();
    });

    // 메시지를 수신하면 콘솔에 출력
    socket.addEventListener("message", (event) => {

    });

    // 연결이 닫히면 콘솔에 출력
    socket.addEventListener("close", (event) => {
        Toastify({
            text: "연결 끊김",
            duration: 1000,
            position: "center",
            style: {
                borderRadius: '20px',
                fontSize: "20px",
            }
        }).showToast();
        startVibrate([5, 50, 50, 300, 10]);
    });

    // 에러가 발생하면 콘솔에 출력
    socket.addEventListener("error", (event) => {
        console.log("Error: " + event);
    });
}

function send_arrow(message) {
    socket.send(message);
}

function send(message) {
    startVibrate(10);
    socket.send(message);
}

function startVibrate(duration) {
    navigator.vibrate(duration);
}

function checkOrientation() {
    const orientationMessage = document.getElementById("orientationMessage");
    const controller = document.getElementById("switch");

    if (window.innerWidth < window.innerHeight) {
        orientationMessage.style.display = "block";
        controller.style.display = "none";
    } else {
        orientationMessage.style.display = "none";
        controller.style.display = "block";
    }
}

// Run on page load
window.onload = function () {
    checkOrientation();
    window.addEventListener("orientationchange", checkOrientation);
    window.addEventListener("resize", checkOrientation);
};