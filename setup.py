from cx_Freeze import setup, Executable

# Define your application
setup(
    name="GenQR",
    version="1.0",
    description="Generate TLV data from JSON and generate TLV text QR",
    executables=[Executable("app.py")],
)
