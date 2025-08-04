#!/bin/bash
# Fix common startup issues

# Fix streamlit.py naming conflict if it exists
if [ -f /home/computeruse/computer_use_demo/streamlit.py ]; then
    echo "Fixing streamlit.py naming conflict..."
    mv /home/computeruse/computer_use_demo/streamlit.py /home/computeruse/computer_use_demo/streamlit_app.py
fi

# Update any references in the entrypoint
if [ -f /home/computeruse/image/entrypoint.sh ]; then
    sed -i 's/streamlit.py/streamlit_app.py/g' /home/computeruse/image/entrypoint.sh
fi

# Ensure proper permissions
chmod -R 755 /home/computeruse/computer_use_demo/

echo "Startup fixes applied successfully"