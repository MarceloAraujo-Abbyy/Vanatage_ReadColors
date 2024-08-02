# Vantage Read Color – Demo APP

## Introduction

Vantage Read Color is a sample demo aplication that enables Vantage to read colors in a document. To use it, you need to configure an image field in Vantage and send this image to the function that counts each colour based on the HSV scale and returns the name of the predominant colour as well as the pixel count of each colour found. 

The function was written in Python, uses OpenCV, and is configured to be published as an Azure function, which makes it possible to integrate it with Vantage.  However is possible you deploy locally or in other cloud providar as AWS. 

After download you can use Visual Code to test and publish it on Azure Function. 

After opening the Application Folder in Visual Code, you need to install the application requirements using the command  pip install -r requeriments.txt

After installing the Python requirements, you can run the application locally to test and understand how it works and make sure all requeriments are installed. 

To do this, there is a "local_test_code" forlder and a "read colour.py" file that must be executed. Select this file on the folder view. Change the name of the test file as in the image below "c://temp//green.png", execute the python script and see the results.

The application returns the dominant color and the number the pixels of each color founded on the image. 

This demo application is set to read a few colours: red, orange, yellow, green, blue and black.  You can change them according to your needs. 

To adjust the colours, you need to know the HSV model. See the reference here on Wiki. https://en.wikipedia.org/wiki/HSL_and_HSV

Based on this model, you should adjust the code by changing the H,S,V values of each colour or by creating new colours.   

Use the test application to make sure it is working as you need, and after update the code on the main function file. 


## Setup Vantage to Use the Function

First you need create a Document Skill to extract the image that you need read the color.

After setup the Document Skill, the Process Skill needs be created, including a custom activity with the code to call the AzureFunction. 

The Code below loops on the all transaction documents, and for each one get the image field, call the read_color function and save the response on the correspondent field. 

The read_color function, converts the image to Base64, call the function and returns the dominant_color parameter. 

```
var docs = Context.Transaction.Documents
for (var doc of docs) {
    if (doc.GetField("New Image 1")) {
        doc.GetField("Color Image 01").Value = read_color(doc.GetField("New Image 1"));
    };
    if (doc.GetField("New Image 2")) {
        doc.GetField("Color Image 02").Value = read_color(doc.GetField("New Image 2"));
    };
    if (doc.GetField("New Image 3")) {
        doc.GetField("Color Image 03").Value = read_color(doc.GetField("New Image 3"));
    };
}

function read_color(f) {
    if (f.Image) {
        var image_base64 = f.Image.ConvertToBase64();
        var data = {"image_base64": image_base64};
        var http_request = Context.CreateHttpRequest();
        http_request.Method= "POST";
        http_request.SetHeader("Content-Type","application/json")
        http_request.Url = "https://<YourApp>.azurewebsites.net/api/<YourFunc>?code="+Context.GetSecret("Azure_Read_Color");
        http_request.SetStringContent(JSON.stringify(data));
        http_request.Send();
        var ret = http_request.ResponseText;
        var obj = JSON.parse(ret);
        return obj["dominant_color"];
    } else {
        return "no image";
    }
}
```

