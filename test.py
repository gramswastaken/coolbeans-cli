import subprocess


if __name__ == "__main__":
    cap_reg = None
    if cap_reg is None:
        sc_data = subprocess.check_output(["grim"])
    else:
        sc_data = subprocess.check_output(["grim", "-g", cap_reg.strip()])
