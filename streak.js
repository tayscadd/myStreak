
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
    //let currentday = document.querySelector('.day-current')
    let all_days = document.querySelectorAll('.week')

    let current_day
    let tomorrow_i
    for (let i=0; i < all_days.length; i++) {
        if (all_days[i].classList.contains('day-current')) {
            current_day = i
        }
    }
    if (all_days.length == current_day) {
        tomorrow_i = 0
    } else {
        tomorrow_i = current_day + 1
    }
    tomorrow_day = all_days[tomorrow_i]
    tomorrow_day.classList.toggle('day-frozen')
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