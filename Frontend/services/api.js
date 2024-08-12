document.addEventListener("DOMContentLoaded", function () {
    let selectedFile;

    // Fotoğraf Yükleme Alanına Tıklama ve Önizleme
    document.getElementById('imageUploadArea').addEventListener('click', function () {
        document.getElementById('imageInput').click();
    });

    // Dosya seçildikten sonra önizleme ve ikonu gizleme
    document.getElementById('imageInput').addEventListener('change', function (event) {
        selectedFile = event.target.files[0];

        if (selectedFile) {
            const reader = new FileReader();

            reader.onload = function (e) {
                const preview = document.getElementById('uploadImagePreview');
                const icon = document.getElementById('uploadIcon');

                preview.src = e.target.result;
                preview.style.display = 'block';
                icon.style.display = 'none';  // İkonu gizle
            };

            reader.readAsDataURL(selectedFile);
        }
    });

    // Request image'e tıklama işlemi (Tahmin yapacak)
    document.getElementById('requestImage').addEventListener('click', async function () {
        if (!selectedFile) {
            document.getElementById('dynamic-text').textContent = 'Lütfen önce bir resim yükleyin.';
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                console.log("Predicted class: ", result.class);

                if (result.class === 'kırmızı') {
                    document.getElementById('dynamic-text').textContent = "It's a red pistachio!";
                } else if (result.class === 'siirt') {
                    document.getElementById('dynamic-text').textContent = "It's a Siirt pistachio!";
                } else {
                    document.getElementById('dynamic-text').textContent = "Unknown pistachio type.";
                }
            } else {
                document.getElementById('dynamic-text').textContent = 'Something went wrong. Please try again.';
            }
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('dynamic-text').textContent = 'An error occurred. Please try again.';
        }
    });
});
