
var client = new XMLHttpRequest();
client.open('GET', '/index.html'); // Replace '/foo.txt' with your file path
client.onreadystatechange = function() {
    if (client.readyState === 4) {
        var fileContents = client.responseText;
        console.log(fileContents); // Display the contents in the console
    }
};
client.send();