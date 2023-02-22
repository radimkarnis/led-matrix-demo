from PIL import Image
import requests

IP = "192.168.33.91"  # <-- Enter the IP of your WLED instance here
URL = f"http://{IP}/json/state"

# Example sprites to be used directly, e.g. `update_matrix(MARIO)`
# Pixels are either grouped (e.g. 5,9,[152,0,0]) - draw pixels 5,6,7,8
# or specified individually (e.g. 9,[152,0,0]) - draw pixel 9
# Pixel can be a list with RGB values or a string with hex represenation
EMPTY = (0,256,[0,0,0])
MARIO = (0,256,[0,0,0], 5,9,[152,0,0], 9,[204,0,0], 10,[255,0,0], 18,21,[152,0,0], 21,23,[204,0,0], 23,27,[255,0,0], 27,[152,0,0], 36,[249,203,156], 38,41,[249,203,156], 41,44,[120,63,4], 50,53,[249,203,156], 53,[102,102,102], 54,58,[249,203,156], 58,[120,63,4], 59,[249,203,156], 60,[120,63,4], 65,68,[249,203,156], 68,[51,51,0], 69,74,[249,203,156], 74,[120,63,4], 75,[249,203,156], 76,[120,63,4], 82,86,[51,51,0], 86,91,[249,203,156], 91,93,[120,63,4], 99,107,[249,203,156], 117,[0,0,255], 118,121,[255,0,0], 121,[0,0,255], 122,124,[255,0,0], 131,134,[255,0,0], 134,[0,0,255], 135,137,[255,0,0], 137,[0,0,255], 138,141,[255,0,0], 146,150,[255,0,0], 150,[255,255,0], 151,153,[0,0,255], 153,[255,255,0], 154,158,[255,0,0], 162,164,[249,203,156], 164,[255,0,0], 165,171,[0,0,255], 171,[255,0,0], 172,174,[249,203,156], 178,181,[249,203,156], 181,187,[0,0,255], 187,190,[249,203,156], 194,196,[249,203,156], 196,199,[0,0,255], 201,204,[0,0,255], 204,206,[249,203,156], 212,215,[0,0,255], 217,220,[0,0,255], 227,231,[120,63,4], 233,237,[120,63,4], 242,247,[120,63,4], 249,254,[120,63,4])
KOOPA = (0,256,[0,0,0], 0,6,[217,217,217], 6,10,[204,0,0], 10,21,[217,217,217], 21,27,[204,0,0], 27,36,[217,217,217], 36,44,[204,0,0], 44,51,[217,217,217], 51,61,[204,0,0], 61,66,[217,217,217], 66,[204,0,0], 69,75,[204,0,0], 77,[204,0,0], 78,81,[217,217,217], 81,84,[204,0,0], 84,[255,255,255], 86,90,[204,0,0], 91,[255,255,255], 92,95,[204,0,0], 95,97,[217,217,217], 97,100,[204,0,0], 100,[255,255,255], 107,[255,255,255], 108,111,[204,0,0], 111,[217,217,217], 112,116,[204,0,0], 116,[255,255,255], 118,[255,255,255], 119,121,[204,0,0], 121,[255,255,255], 123,[255,255,255], 124,132,[204,0,0], 132,135,[255,255,255], 135,137,[204,0,0], 137,140,[255,255,255], 140,160,[204,0,0], 160,[217,217,217], 161,166,[204,0,0], 166,170,[255,204,153], 170,175,[204,0,0], 175,180,[217,217,217], 180,189,[255,204,153], 189,194,[217,217,217], 196,205,[255,204,153], 205,209,[217,217,217], 214,219,[255,204,153], 222,225,[217,217,217], 231,234,[255,204,153], 238,242,[217,217,217], 247,249,[217,217,217], 253,256,[217,217,217])
HASS = (0,256,[0,0,0], 0,23,[0,176,240], 23,25,[255,255,255], 25,38,[0,176,240], 38,42,[255,255,255], 42,53,[0,176,240], 53,59,[255,255,255], 59,68,[0,176,240], 68,72,[255,255,255], 72,[0,176,240], 73,76,[255,255,255], 76,83,[0,176,240], 83,87,[255,255,255], 87,[0,176,240], 88,[255,255,255], 89,[0,176,240], 90,93,[255,255,255], 93,98,[0,176,240], 98,104,[255,255,255], 104,[0,176,240], 105,110,[255,255,255], 110,113,[0,176,240], 113,116,[255,255,255], 116,[0,176,240], 117,120,[255,255,255], 120,[0,176,240], 121,127,[255,255,255], 127,[0,176,240], 128,131,[255,255,255], 131,[0,176,240], 132,[255,255,255], 133,[0,176,240], 134,136,[255,255,255], 136,[0,176,240], 137,139,[255,255,255], 139,[0,176,240], 140,144,[255,255,255], 144,146,[0,176,240], 146,148,[255,255,255], 148,[0,176,240], 149,152,[255,255,255], 152,[0,176,240], 153,[255,255,255], 154,[0,176,240], 155,[255,255,255], 156,[0,176,240], 157,[255,255,255], 158,162,[0,176,240], 162,165,[255,255,255], 165,167,[0,176,240], 167,[255,255,255], 168,[0,176,240], 169,171,[255,255,255], 171,[0,176,240], 172,174,[255,255,255], 174,178,[0,176,240], 178,183,[255,255,255], 183,185,[0,176,240], 185,[255,255,255], 186,[0,176,240], 187,190,[255,255,255], 190,194,[0,176,240], 194,200,[255,255,255], 200,202,[0,176,240], 202,206,[255,255,255], 206,210,[0,176,240], 210,216,[255,255,255], 216,[0,176,240], 217,222,[255,255,255], 222,256,[0,176,240])
ESPRESSIF = [0, '000000', 1, '000000', 2, '010101', 3, '010000', 4, '010101', 5, '4c0d0f', 6, '020101', 7, '611317', 8, 'd8342c', 9, 'd0312b', 10, 'd0312b', 11, '9c2520', 12, '32090a', 13, '010000', 14, '000000', 15, '000000', 16, '000000', 17, '1a0605', 18, 'aa2724', 19, '140202', 20, '420908', 21, 'cc2d25', 22, 'de352d', 23, 'bd2e2a', 24, '1b0303', 25, '200302', 26, 'ba2923', 27, 'e6372b', 28, 'dd342c', 29, '721a19', 30, '000101', 31, '000000', 32, '020101', 33, 'b52f2a', 34, '550f0f', 35, '180101', 36, '6f140f', 37, 'e8352b', 38, 'e8362c', 39, 'e8362c', 40, 'e8352b', 41, '61110e', 42, '110202', 43, '5f100d', 44, 'e7362b', 45, 'e4332a', 46, '721813', 47, '010101', 48, '5d1212', 49, 'c42d28', 50, '010101', 51, '000000', 52, '0f0101', 53, '000000', 54, '420807', 55, 'e4342c', 56, 'e8362c', 57, 'e8362b', 58, '7d1915', 59, '110202', 60, '5f110f', 61, 'e7372c', 62, 'da352d', 63, '3b0a0d', 64, 'b22c25', 65, '490d0d', 66, '000000', 67, 'ac2621', 68, 'd22f2b', 69, '7d1b14', 70, '000000', 71, '000000', 72, '3e0806', 73, 'e7352c', 74, 'e8362c', 75, 'af261f', 76, '180202', 77, '891d19', 78, 'e8352c', 79, '9c241e', 80, 'c12b28', 81, '210302', 82, '590f0a', 83, 'e8362c', 84, 'e8362c', 85, 'e8362b', 86, 'e8362c', 87, 'd63028', 88, '220303', 89, '3b0708', 90, 'e4352b', 91, 'e8362c', 92, '9d261d', 93, '090202', 94, '9c201a', 95, 'd02f2a', 96, 'c22e29', 97, '420908', 98, 'de332a', 99, 'dc322b', 100, '971f1b', 101, '7f1a17', 102, 'd32f26', 103, 'e8362c', 104, 'db3229', 105, '260303', 106, '420908', 107, 'e9352c', 108, 'e8362c', 109, '831b18', 110, '2d0404', 111, 'e5362d', 112, 'ca3029', 113, '280404', 114, 'de332a', 115, 'e2352b', 116, 'a32520', 117, '2c0404', 118, '230303', 119, 'bc2924', 120, 'e8362c', 121, 'e8352c', 122, '060101', 123, '4a0b08', 124, 'e8362c', 125, 'cc2e25', 126, '000000', 127, 'bf2d25', 128, 'c9312c', 129, '220404', 130, '63100d', 131, 'e9362c', 132, 'e8362c', 133, 'e7362c', 134, '631210', 135, '000000', 136, '7b1813', 137, 'e8362c', 138, '7e1a15', 139, '280707', 140, 'd83329', 141, 'e9362c', 142, '6b1413', 143, '1e0404', 144, 'c8302a', 145, '0e0404', 146, '0f0101', 147, '410908', 148, 'b62a21', 149, 'e9362c', 150, 'e9362d', 151, '5f110e', 152, '250404', 153, 'e8362c', 154, 'e7362c', 155, '450b08', 156, '580f0c', 157, 'e8362c', 158, 'ca2e29', 159, '010101', 160, '96231e', 161, '92211e', 162, '010101', 163, '1b0203', 164, '1d0304', 165, '58110f', 166, 'e7362c', 167, 'e6362c', 168, '320804', 169, '7d1a14', 170, 'e8362c', 171, '6b150f', 172, '1a0202', 173, 'e8362c', 174, 'e8352b', 175, '380b0f', 176, '420908', 177, 'cc312c', 178, '1d0b0a', 179, 'db332d', 180, 'dc3129', 181, '200403', 182, 'dd352d', 183, 'e8362c', 184, '420908', 185, '350604', 186, 'e7362c', 187, 'c93128', 188, '300403', 189, 'cb2d25', 190, 'b62b24', 191, '020102', 192, '010000', 193, '832220', 194, 'b32d28', 195, 'cb302a', 196, 'e3342c', 197, '230303', 198, 'ba2c25', 199, 'e8362c', 200, '7d1a14', 201, '280302', 202, 'e8362c', 203, 'cb2d25', 204, '370a08', 205, '7d1e1c', 206, '260708', 207, '000000', 208, '000000', 209, '420908', 210, '95221b', 211, 'b52e27', 212, '170605', 213, '1a0a0b', 214, '520d0a', 215, 'cb2e25', 216, '510e0b', 217, '000000', 218, 'de3128', 219, '360604', 220, '010101', 221, '5d1415', 222, 'a22420', 223, '030203', 224, '000000', 225, '000000', 226, '3b0807', 227, '7a1a19', 228, 'c7302d', 229, '320707', 230, '230402', 231, '210302', 232, '110201', 233, '150303', 234, '260403', 235, '2a0707', 236, 'aa2621', 237, 'c02d28', 238, '3c0a0a', 239, '010000', 240, '000000', 241, '000000', 242, '000000', 243, '3b0706', 244, '420908', 245, '9a2421', 246, 'b92d27', 247, 'c42d29', 248, 'bd2822', 249, 'c52e27', 250, 'ac2a24', 251, 'bd2b25', 252, '721817', 253, '420908', 254, '000000', 255, '000000']


def update_matrix(sprite, bri=100, on=True):
    """Send data to the LED matrix"""
    data = {"on": on, "bri": bri, "seg": {"i": sprite}}
    post = requests.post(URL, json=data)
    if post.status_code != 200:
        print(f"Fail: {post.text}")


def from_img(path):
    """Convert a .bmp or .png image to LED matrix data"""
    img = Image.open(path)
    pixels = img.getdata()
    pixels = [pixel[:3] for pixel in pixels]  # RGBW -> strip the W
    data = []
    for pixel_index, pixel in enumerate(pixels):
        data.append(pixel_index)
        data.append(f"{pixel[0]:02x}{pixel[1]:02x}{pixel[2]:02x}")
    return data


# Display preset MARIO on the matrix with brightness set to 100
# update_matrix(MARIO)
# Display `my_image.bmp` on the matrix with brightness set to 57
# update_matrix(from_img("my_image.bmp"), 57)
