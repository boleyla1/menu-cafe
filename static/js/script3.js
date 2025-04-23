$(document).ready(function() {
    // افزودن محصول جدید
    $('#productForm').on('submit', function(e) {
        e.preventDefault();
        this.submit();
    });

    // باز کردن مودال ویرایش
    window.openEditModal = function(id, name, description, price, imageUrl, categoryId) {
        $('#editProductForm').attr('action', `/products/update/${id}/`);
        $('#editProductName').val(name);
        $('#editProductDescription').val(ingredients);
        $('#editProductPrice').val(price);
        $('#editProductCategory').val(categoryId);
        $('#editImagePreview').attr('src', imageUrl ? imageUrl : '');
        $('#editModal').fadeIn();
    }

    // بروزرسانی محصول
    window.updateProduct = function() {
        $('#editProductForm').submit();
    }

    // باز کردن مودال تایید حذف
    window.openDeleteModal = function(id) {
        $('#deleteProductForm').attr('action', `/products/delete/${id}/`);
        $('#deleteModal').fadeIn();
    }
    // یاز کردن مودال تایید حذف
    $(document).ready(function (){
        window.openDeleteModal = function (id){
            $('#deleteProductFormm').attr('action',`/products/delete/${id}/`);
            $('deleteModal').fadeIn();
        }
    })
    // بستن مودال‌ها
    window.closeModal = function(modalId) {
        $('#' + modalId).fadeOut();
    }

    // بستن مودال‌ها با کلیک بیرون از مودال
    $(window).on('click', function(event) {
        if ($(event.target).hasClass('modal')) {
            $(event.target).fadeOut();
        }
    });
});