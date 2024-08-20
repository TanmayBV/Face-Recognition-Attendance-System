### Training:
- Make folder `training-images`.
- Add images of each person you want to recognise to a folder by their name in `training-images`.

    Example
    ```bash
    $ mkdir training-images
    $ cd training-images
    $ mkdir Name_Of_Person
    ```
    Then copy all the images of that person in `./training-images/Name_Of_Person` folder.

    <img src='https://user-images.githubusercontent.com/17249362/28241803-2b6db474-69b9-11e7-9a70-43fd3e9b30a7.png' width='300px'>

- Run on cmd `python create_encodings.py` to get the encodings of the images and the labels.
    This will create `encoded-images-data.csv` and `labels.pkl` files.

    <img src='https://user-images.githubusercontent.com/17249362/28241799-1a848d7c-69b9-11e7-8572-dbac69631085.png' width='700px'>

    Note: There has to be only one face per image otherwise encoding will be for the first face found in the image.

- Run on cmd `python train.py` to train and save the face recognition classifier.
    This will create `classifier.pkl` file.
    It will also create `classifier.pkl.bak` backup file if the classifier with that name already exists.

    <img src='https://user-images.githubusercontent.com/17249362/28241802-2894f456-69b9-11e7-91e8-341115fba605.png' width='700px'>

### Prediction:
- Make folder `test-images` which contains all the images you want to find people in.

    <img src='https://user-images.githubusercontent.com/17249362/28241801-25db4814-69b9-11e7-9c8e-c19f3e09499a.png' width='300px'>

- Run on cmd `python predict.py` to predict the faces in each image.

    <img src='https://user-images.githubusercontent.com/17249362/28241800-21ecf69e-69b9-11e7-8564-6d9dcb067225.png' width='700px'>
