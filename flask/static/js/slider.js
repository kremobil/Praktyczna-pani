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
    console.log(slide_number)
    photo = "url('../static/img/slide" + slide_number + ".jpg')"
    const slide = document.getElementsByClassName("slide")[0]
    slide.style.backgroundImage = photo;
    for (let i = 0; i < 100; i++){

        setTimeout(printI(i),1000);

    }
}

//
//const slide = document.getElementsByClassName("slide")[0]
//slide.style.backgroundImage = photo;
//const slider = document.getElementsByClassName("slider")[0]
//slider.style.backgroundImage = 'url("../static/img/slide1.jpg")';

