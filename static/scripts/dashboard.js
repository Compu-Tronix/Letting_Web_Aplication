function toggleUploadForm() {
    document.getElementById('information-container').innerHTML =
    `
    <div class="listing_form">
        <form action="/list_item/" method="POST" enctype="multipart/form-data">
            <input type="text" placeholder="name of item" name="item_name" required>
            <input type="text" placeholder="model description" name="model_description" required>
            <input type="number" placeholder="price per 24hrs" name="price" required>
            <input type="file" placeholder="upload item image" name="item_img" required>
            <input type="submit" value="upload">
        </form>
    </div>
    
    `
}