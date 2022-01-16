from PIL import Image


def func():
    img = Image.open('img/dogo.jpeg')
    img = Image.open('img/dogo.jpeg')
    print(img.format)
    print(img.size)
    print(img.mode)
    img.save('test.jpg')
    
    
if __name__ == '__main__':
    func()
    