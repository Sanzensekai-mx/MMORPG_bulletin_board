let imgTag = document.getElementsByClassName("image-wrapper")[0].children[0];

let curSliderPos = 0

let imgList = document.querySelectorAll(".media")
console.log(imgList)

function validPosition(direction, pictList) {
    let imgTag = document.getElementsByClassName("image-wrapper")[0].children[curSliderPos]
    console.log(imgTag)
    if (direction === 'forward') {
        curSliderPos++
    } else if (direction === 'back') {
        curSliderPos--
    }
    if (curSliderPos < 0) {
        curSliderPos = pictList.length + curSliderPos
    } else if (curSliderPos > pictList.length - 1) {
        curSliderPos = 0
    }
    let previosImgTag = imgTag;
    console.log(previosImgTag)
    imgTag = document.getElementsByClassName("image-wrapper")[0].children[curSliderPos]
    console.log(imgTag)
    return [imgTag, previosImgTag]
}

function changeClassAnimation(direction, previosImg, curImg) {
    if (direction === 'forward') {
        curImg.setAttribute('class', 'right')
        previosImg.setAttribute('class', null)
    } else if (direction === 'back') {
        curImg.setAttribute('class', 'left')
        previosImg.setAttribute('class', null)
    }
}

function stepHandler(direction) {
    let [imgTag, previosImgTag] = validPosition(direction, imgList)
    previosImgTag.style.display = 'none'
    imgTag.style.display = 'block'
    changeClassAnimation(direction, previosImgTag, imgTag)
}

document.getElementsByClassName("slider-btn-forward")[0].addEventListener('click', function (e) {
        stepHandler('forward')
}, false);

document.addEventListener('keydown', function (e) {
    if (e.code === "ArrowRight") {
    stepHandler('forward')
    }
}, false);

document.getElementsByClassName("slider-btn-back")[0].addEventListener('click', function(e) {
        stepHandler('back')
}, false);

document.addEventListener('keydown', function (e) {
    if (e.code === "ArrowLeft") {
    stepHandler('back')
    }
}, false);

document.getElementsByClassName("slider-btn-forward")[1].addEventListener('click', function(e) {
        stepHandler('forward')
}, false);

document.getElementsByClassName("slider-btn-back")[1].addEventListener('click', function(e) {
        stepHandler('back')
}, false);


function deletePreviousModeImg() {
    let imgWrapTag = document.getElementsByClassName("image-wrapper")[0];
    while (imgWrapTag.firstChild) {
        imgWrapTag.removeChild(imgWrapTag.firstChild);
      }
    }