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

    let i = 1;

    function increment() {
       i = i - 0.01;
       slide.style.opacity = i;
    }

    let timer = setTimeout(function myTimer() {
       increment();

       timer = setTimeout(myTimer, 10);
    }, 10);

    setTimeout(() => {
    slide.style.opacity = 0;
    clearTimeout(timer); }, 1000);

    opacityslide()

}

function opacityslide(){
    slide.style.backgroundImage = photo;
    slide.style.opacity = 1;
}
//
//const slide = document.getElementsByClassName("slide")[0]
//slide.style.backgroundImage = photo;
//const slider = document.getElementsByClassName("slider")[0]
//slider.style.backgroundImage = 'url("../static/img/slide1.jpg")';

