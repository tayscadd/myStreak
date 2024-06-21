
function increaseCounter() {
    let streak_counter = document.querySelector('#streakCounter')
    let streak_img = document.querySelector('.img-streak')
    count = Number(streak_counter.innerHTML) + 1
    streak_counter.innerHTML = count
    if (count > 0 && streak_img.classList.contains('img-streak-active') == false) {
        streak_img.classList.add('img-streak-active')
    }
}
function decreaseCounter() {
    let streak_counter = document.querySelector('#streakCounter')
    let streak_img = document.querySelector('.img-streak')
    count = Number(streak_counter.innerHTML) - 1
    if (count < 0) {
        count = 0
    } 
    if (count <= 0) {
        streak_img.classList.remove('img-streak-active')
    }
    streak_counter.innerHTML = count
}
function freeze() {
    let a = 1
}
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}
/*
function toggle_day_streak(day) {
    if (day.classList.contains('ongoing-streak')) {
        decreaseCounter()
    } else {
        increaseCounter()
    }
    day.classList.toggle('ongoing-streak')
}
sleep(1000).then(() => {
    days = document.querySelectorAll('.week')

    days.forEach(day => {
        day.addEventListener('click', () => {
            toggle_day_streak(day)
        })
    })
    console.log(days)
})
*/