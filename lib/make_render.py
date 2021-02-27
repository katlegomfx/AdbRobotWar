import cv2

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def window(name='test', data=None, wid=640, ml=False):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    data = ResizeWithAspectRatio(data, wid)
    cv2.imshow(name, data)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyWindow(name)
        return 'close'
    # if ml:
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         cv2.destroyAllWindows()
            
    # else:
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         cv2.destroyWindow(name)