/*!
* Start Bootstrap - Blog Home v5.0.9 (https://startbootstrap.com/template/blog-home)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-blog-home/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project


document.addEventListener('DOMContentLoaded', function() {
    // Находим кнопку "Добавить изображение"
    var addButton = document.getElementById('add-image');

    // Находим контейнер для полей ввода изображений
    var imageFields = document.getElementById('image-fields');

    // Устанавливаем начальное количество полей ввода изображений
    var fieldCount = 0;

    // Добавляем обработчик события клика на кнопку "Добавить изображение"
    addButton.addEventListener('click', function() {
        // Создаем новый элемент поля ввода изображения
        var newField = document.createElement('div');
        newField.className = 'form-group';
//        newField.innerHTML = '<label for="id_image-' + fieldCount + '">Image ' + fieldCount + '</label><input type="file" name="image-' + fieldCount + '" class="form-control-file">';
        newField.innerHTML = '<label for="id_image-' + fieldCount + '">Image ' + fieldCount + '</label><input type="file" name="images" class="form-control-file">';
        // Добавляем новое поле ввода в контейнер
        imageFields.appendChild(newField);

        // Увеличиваем счетчик количества полей ввода изображений
        fieldCount++;
    });
});

document.addEventListener('DOMContentLoaded', function() {
    let deleteButtons = document.getElementsByClassName('delete-image')
    console.log(deleteButtons)
    let deletedArray = new Array();
    let imagesElements = document.getElementsByClassName('image-div')

    function updateDeletedInput() {
        const deletedImagesInput = document.getElementById('deleted-images-input');
        deletedImagesInput.value = JSON.stringify(deletedArray);
    }

    for (let i = 0; i < imagesElements.length; i++) {
        const image = imagesElements[i]
        const button = deleteButtons[i]
        button.addEventListener('click', () => {
            image.remove();
            deletedArray.push(i)
            console.log(i)
            console.log(deletedArray)
            updateDeletedInput();
        })
    }

    
})

