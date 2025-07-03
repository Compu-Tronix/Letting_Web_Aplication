//
// app.html catagory functions
//

// catagoryOne ()
function catagoryOne() {
    document.getElementById('productContainer').innerHTML = `
    
    {% for catagoryOne in catagory %}
    <h1>
        {{ catagoryOne }}
    </h1>
    {% endfor %}

    `
}