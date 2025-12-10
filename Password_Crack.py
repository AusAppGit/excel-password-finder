import itertools
import msoffcrypto
import string
import subprocess
import os


def main():
    print("Select the file extension:")
    which = int(input(
        "1 = .docx/.xlsx (Numerical), 2 = .docx/.xlsx (Alphabetical) , 3 = Alphanumerical\n"
        "Stop! : "))
    if which == 1:
        try:
            file_docx = str(input("Which DOCX/XLSX-File?\n"))
            if is_decrypt(file_docx):
                decrypt_docx(file_docx, alpha=False)
            else:
                print("File might not be encryted.")
        except:
            print("Error! Have you entered the whole path?")
    elif which == 2:
        try:
            file_docx = str(input("Which DOCX/XLSX-File?\n"))
            if is_decrypt(file_docx):
                decrypt_docx(file_docx, alpha=True)
            else:
                print("File might not be encryted.")
        except:
            print("Error! Have you entered the whole path?")
    elif which == 3:
        try:
            file_gpg = str(input("Which File?\n"))
            if is_decrypt(file_gpg):
                decrypt_gpg(file_gpg)
            else:
                print("File might not be encryted.")
        except:
            print("Error! Have you entered the whole path?")
    else:
        print("Encryption not implemented yet")
    # print("Press any key to continue...")

def is_decrypt(file_path: str):
    print("Checking for encryption...")
    filePath = "msoffcrypto-tool " + file_path + " --test -v"
    result = subprocess.run(filePath, capture_output=True, text=True)
    if result.returncode == 1:
        print("File is not encrypted")
        return False
    elif result.returncode == 0:
        print("Encrytped File test")
        return True
    else:
        print("An error occurred checking the file.")


def decrypt_docx(file_docx: str, alpha):
    file_docx = file_docx.replace('\"', "")
    if os.path.exists(file_docx):
        print("Found the file.")
    else:
        print("Something is wrong, could be with your path or filename.")
        exit()

    chars = string.digits
    if alpha:
        chars = string.ascii_letters + string.digits
    attempts = 0
    # print that you can go shopping :D
    print("Trying to open the file. This may take a while...")
    for plen in range(1, 9):  # already the same
        for guess in itertools.product(chars, repeat=plen):
            attempts += 1
            guess = ''.join(guess)
            print(f"Guess: {guess}, Attempt No: {attempts}", end='\r')
            # print(guess,attempts)                                          #Debug
            try:
                # try start msoffcrypto-tool as OfficeFile with
                file = msoffcrypto.OfficeFile(open(file_docx, "rb"))
                # file-name and read-access only
                # if password required, take the generated
                file.load_key(password=guess)
                file.decrypt(open("decrypted.docx", "wb"))
                print(
                    "[DOCX, XLSX BRUTE-FORCE]: found password! password: {} with {} attempts".format(guess, attempts))
                return True
            except:
                # print(str(attempts)+"not correct!")                        #Debug
                continue  # otherwise continue with next password


def decrypt_gpg(file_gpg):
    chars = string.ascii_letters + string.digits + string.punctuation
    attempts = 0
    # print that you can go shopping :D
    print("Searching for password!\nThis may take a long time...")
    for plen in range(1, 9):  # already the same
        for guess in itertools.product(chars, repeat=plen):
            attempts += 1
            guess = ''.join(guess)
            print(f"Guess: {guess}, Attempt No: {attempts}", end='\r')
            # print(guess,attempts)                                          #Debug
            try:
                # try get true by using function checkPassword which use the file
                if checkPassword(file_gpg, guess):
                    # as file_gpg and generated password
                    print("[GPG BRUTE-FORCE]: found password! "
                          "password: {} with {} attempts".format(guess, attempts))  # print success!
                    return True
            except:
                # print(str(attempts)+" not correct!")                       #Debug
                continue  # otherwise next password


# function to check password from gpg-encrypted files
def checkPassword(filename, password):
    output = ""
    try:  # try create new subprocess with check_output function. Execute command at shell.
        # gpg = start gpg, --pinentry-mode loopback = send a password directly to GnuPG,
        # rather than GnuPG itself prompting for the password.
        # --output decrypted_gpg.txt = after decryption save it decrypted in txt-file
        # --batch --yes = execute int batch true
        # --passphrase password = generated password from function decrypt_gpg()
        # -d filename = encrypted file to decrypt
        # shell = True --> open in shell
        subprocess.check_output(
            "gpg --pinentry-mode loopback --output decrypted_gpg.txt --batch --yes --passphrase " + password +
            " -d " + filename + " 2>&1", shell=True)
        return True  # if executed without errors return True and password was correct
    except subprocess.CalledProcessError as e:  # if subprocess-error you can print it out
        # out = str(e.output)                                                #Debug
        # print(out)                                                         #Debug
        return False  # password wasn't correct
    except:
        return False  # if other error return False --> next password


if __name__ == "__main__":  # declare function main() as first executed function
    main()
