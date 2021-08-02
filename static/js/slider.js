function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}
var slide_number = 1
var photo = "url('../static/img/slide" + slide_number + ".jpg')"
const slide = document.getElementsByClassName("slide")[0]
const slider = document.getElementsByClassName("slider")[0]
const button = document.getElementsByClassName("arrow")[0]
const button2 = document.getElementsByClassName("arrowsecound")[0]
slide.style.backgroundImage = photo;
console.log(photo)

function printI(i){
    console.log(i)
}
function slide_change(increase){
    slide_number += increase
    if (slide_number == 0){
    slide_number = 5
    }
    if (slide_number == 6){
    slide_number = 1
    }
    photo = "url('../static/img/slide" + slide_number + ".jpg')"
    slider.style.backgroundImage = photo;
    button.style.display = "none";
    button2.style.display = "none";
    slide.style.animationName = "fader";
    wait(980, 1.5, photo, slide, button, button2);


}

function wait(time, repeat, photo, slide, button, button2){
    let i = 0;

    function increment() {
       i++;
       console.log(i);
    }

    let timer = setTimeout(function myTimer() {
       increment();
       timer = setTimeout(myTimer, time);
    }, time);

    setTimeout(() => {
    slide.style.backgroundImage = photo;
    slide.style.animationName = ''
    button.style.display = "block";
    button2.style.display = "block";
    clearTimeout(timer); }, repeat * time);
}

//
//const slide = document.getElementsByClassName("slide")[0]
//slide.style.backgroundImage = photo;
//const slider = document.getElementsByClassName("slider")[0]
//slider.style.backgroundImage = 'url("../static/img/slide1.jpg")';

