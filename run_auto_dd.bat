
IF EXIST .env\ (
.env\Scripts\activate.bat
) ELSE (
echo "WARN: You do not have a virtual environment. Have you ran install_requirements.bat?"
echo "Things might explode in a spectacular fashion"
)

python -u main.py

IF EXIST .env\ (
.env\Scripts\deactivate.bat
)

exit