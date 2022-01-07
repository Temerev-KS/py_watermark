from PIL import Image


def func():
    img = Image.open('img/dogo.jpeg')
    print(img.format)
    print(img.size)
    print(img.mode)
    img.show()
    
    
if __name__ == '__main__':
    func()
    