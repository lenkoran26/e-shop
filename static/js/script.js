    
 
  function updateSubcategories() {
    // Получаем выбранную категорию
    var category = document.getElementById('category').value;
    // Получаем список подкатегорий для выбранной категории из контекста
    var subcategories = categories[category].subcategories;
 
    // Обновляем список подкатегорий в поле выбора подкатегории
    var subcategorySelect = document.getElementById('subcategory');
    subcategorySelect.innerHTML = '';
    for (var i = 0; i < subcategories.length; i++) {
      var option = document.createElement('option');
      option.value = subcategories[i];
      option.text = subcategories[i];
      subcategorySelect.appendChild(option);
    }
  };
 
  // Вызываем функцию при загрузке страницы и при изменении значения в поле выбора категории
  window.onload = updateSubcategories;
  document.getElementById('category').addEventListener('change', updateSubcategories);


