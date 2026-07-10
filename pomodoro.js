const timeInput = document.querySelector("#time-input")
const startBtn = document.querySelector("#start-timer")
const stopBtn = document.querySelector("#stop-timer")
const display = document.querySelector("#timer-display")

// 남은 시간
let remainingSeconds = 0

// 현재 동작 중인 타이머 id
let timerId = null;

// 남은 시간을 보여주는 함수
function updateDisplay() {
    // 60으로 나눈 몫
    const min = Math.floor(remainingSeconds / 60)

    // 60으로 나눈 나머지
    const sec = remainingSeconds % 60

    // min = 1 & sec = 1 => 01:01
    const timeToDisplay =
        String(min).padStart(2, "0") + ":" +
        String(sec).padStart(2, "0")

    display.textContent = timeToDisplay
}

// 타이머 시작
startBtn.addEventListener("click", () => {
    const minutes = Number(timeInput.value)
    if (Number.isNaN(minutes) || minutes <= 0) {
        alert("올바른 시간(분)을 입력해주세요.")
        return
    }

    remainingSeconds = minutes * 60
    updateDisplay()

    // 초 단위 카운트다운 시작
    timerId = setInterval(
        () => {
            remainingSeconds--

            if (remainingSeconds <= 0) {
                clearInterval(timerId)
                alert("타이머 종료!")
            }

            updateDisplay()
        },
        1000
    )
})

stopBtn.addEventListener("click", () => {
    clearInterval(timerId)
})