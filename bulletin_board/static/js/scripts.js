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
        newField.innerHTML = '<label for="id_images-' + fieldCount + '">Image ' + fieldCount + '</label><input type="file" name="images-' + fieldCount + '" class="form-control-file">';

        // Добавляем новое поле ввода в контейнер
        imageFields.appendChild(newField);

        // Увеличиваем счетчик количества полей ввода изображений
        fieldCount++;
    });
});