from microbit import i2c
import utime

I2C_CMD_CONTINUE_DATA = 0x81

GROVE_TWO_RGB_LED_MATRIX_DEF_I2C_ADDR = 0x65 # L'adresse i2c de l'appareil par défaut
GROVE_TWO_RGB_LED_MATRIX_VID = 0x2886 # ID de fournisseur de l'appareil
GROVE_TWO_RGB_LED_MATRIX_PID = 0x8005 # ID produit de l'appareil

I2C_CMD_GET_DEV_ID = 0x00 # Cette commande obtient les informations d'ID de périphérique
I2C_CMD_DISP_BAR = 0x01 # Cette commande affiche la barre de LED
I2C_CMD_DISP_EMOJI = 0x02 # Cette commande affiche les emoji
I2C_CMD_DISP_NUM = 0x03 # Cette commande affiche le numéro
I2C_CMD_DISP_STR = 0x04 # Cette commande affiche la chaîne
I2C_CMD_DISP_CUSTOM = 0x05 # Cette commande affiche les images définies par l'utilisateur
I2C_CMD_DISP_OFF = 0x06 # Cette commande nettoie l'affichage
I2C_CMD_DISP_ASCII = 0x07 # ne pas utiliser
I2C_CMD_DISP_FLASH = 0x08 # Cette commande affiche les images qui sont stockées en flash
I2C_CMD_DISP_COLOR_BAR = 0x09 # Cette commande affiche une barre de led colorée
I2C_CMD_DISP_COLOR_WAVE = 0x0a # Cette commande affiche l'animation d'onde intégrée
I2C_CMD_DISP_COLOR_CLOCKWISE = 0x0b # Cette commande affiche l'animation intégrée dans le sens des aiguilles d'une montre
I2C_CMD_DISP_COLOR_ANIMATION = 0x0c # Cette commande affiche une autre animation intégrée
I2C_CMD_DISP_COLOR_BLOCK = 0x0d # Cette commande affiche une couleur définie par l'utilisateur
I2C_CMD_STORE_FLASH = 0xa0 # Cette commande stocke les trames en flash
I2C_CMD_DELETE_FLASH = 0xa1 # Cette commande supprime toutes les trames en flash

I2C_CMD_LED_ON = 0xb0 # Cette commande allume le mode flash de l'indicateur LED
I2C_CMD_LED_OFF = 0xb1 # Cette commande éteint le mode flash de l'indicateur LED
I2C_CMD_AUTO_SLEEP_ON = 0xb2 # Cette commande active le mode veille automatique de l'appareil
I2C_CMD_AUTO_SLEEP_OFF = 0xb3 # Cette commande désactive le mode veille automatique de l'appareil (mode par défaut)

I2C_CMD_DISP_ROTATE = 0xb4 # Cette commande définit l'orientation de l'affichage
I2C_CMD_DISP_OFFSET = 0xb5 # Cette commande définit le décalage d'affichage

I2C_CMD_SET_ADDR = 0xc0 # Cette commande définit l'adresse i2c du périphérique
I2C_CMD_RST_ADDR = 0xc1 # Cette commande réinitialise l'adresse i2c du périphérique
I2C_CMD_TEST_TX_RX_ON = 0xe0 # Cette commande active le mode de test de la broche TX RX
I2C_CMD_TEST_TX_RX_OFF = 0xe1 # Cette commande désactive le mode de test de la broche TX RX
I2C_CMD_TEST_GET_VER = 0xe2 # Cette commande est utilisée pour obtenir la version du logiciel
I2C_CMD_GET_DEVICE_UID = 0xf1 # Cette commande est utilisée pour obtenir l'identifiant de la puce

orientation_type_t = {
  'DISPLAY_ROTATE_0': 0,
  'DISPLAY_ROTATE_90': 1,
  'DISPLAY_ROTATE_180': 2,
  'DISPLAY_ROTATE_270': 3
}

COULEURS = {
  'rouge': 0x00,
  'orange': 0x12,
  'jaune': 0x18,
  'vert': 0x52,
  'cyan': 0x7f,
  'bleu': 0xaa,
  'violet': 0xc3,
  'rose': 0xdc,
  'blanc': 0xfe,
  'noir': 0xff
}

class GroveTwoRGBLedMatrix(object):
    def __init__(self, base=GROVE_TWO_RGB_LED_MATRIX_DEF_I2C_ADDR, screenNumber=1):
        self.offsetAddress = screenNumber - 1
        self.baseAddress = base
        self._addr = self.offsetAddress + self.baseAddress

    def displayFrames(self, buffer, duration_time, forever_flag, frames_number):
        data = bytearray(72)
        # max 5 frames in storage
        if frames_number > 5:
            frames_number = 5
        elif frames_number == 0:
            return

        data[0] = I2C_CMD_DISP_CUSTOM
        data[1] = 0x00
        data[2] = 0x00
        data[3] = 0x00
        data[4] = frames_number

        for i in range(frames_number - 1, -1, -1):
            data[5] = i
            # different from uint8_t buffer
            for j in range(8):
                for k in range(7, -1, -1):
                    data[8 + j * 8 + (7 - k)] = buffer[j * 8 + k + i * 64]

            if i == 0:
                # display when everything is finished.
                data[1] = duration_time & 0xff
                data[2] = (duration_time >> 8) & 0xff
                data[3] = forever_flag
            i2c.write(self._addr, data)
            utime.sleep_ms(1)  # Adjust the delay as needed

    def stopDisplay(self):
        i2c.write(self._addr, bytes([I2C_CMD_DISP_OFF]))