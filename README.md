# QR Viewer – GDS‑based QR‑code sample tracker

A Django‑powered web app that lets you

* **Upload GDSII QR Code Layouts** and automatically characterize the characteristics of the file 
* **Upload sample images** (individually or as a ZIP) containing qr codes to automatically associate with a location
* **Detect the QR codes** in each image, locate their absolute coordinates and match them to the GDS design  
* **Visual‑inspect the grid** of QR positions, zoom & pan, and click a cell to see every sample image that hits that code  
* **Debug the scanner** — press **Submit and Debug** to get a live overlay of every QR found, shown in a popup modal

Run with python manage.py runserver
