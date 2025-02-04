If **PyPI is blocked** due to network restrictions (such as a corporate proxy), you need to configure **PCF to use a proxy** when installing dependencies.

---

## **Solution: Whitelist Proxy in PCF for `requirements.txt`**
Since PCF does not directly allow setting proxy configurations inside `requirements.txt`, follow these steps:

---

### **1. Set Proxy Environment Variables in `manifest.yml`**
Modify your `manifest.yml` to include the proxy settings:

```yaml
applications:
  - name: my-python-api
    memory: 512M
    instances: 1
    buildpacks:
      - python_buildpack
    command: gunicorn app:app -b 0.0.0.0:$PORT
    env:
      HTTP_PROXY: http://your-proxy-server:port
      HTTPS_PROXY: http://your-proxy-server:port
      NO_PROXY: localhost,127.0.0.1
```

Replace:
- `http://your-proxy-server:port` with your **proxy URL**.

---

### **2. Manually Install Dependencies Before Deployment**
If your PCF environment doesn't allow direct PyPI access, **manually download dependencies** and deploy them with your app.

#### **Download Dependencies Locally**
Run this on a machine with internet access:

```sh
pip download -r requirements.txt -d vendor/
```

#### **Modify `requirements.txt`**
Update `requirements.txt` to use local packages:

```
--find-links vendor/
flask
gunicorn
```

#### **Update `manifest.yml`**
Ensure your app uses the vendored packages:

```yaml
applications:
  - name: my-python-api
    memory: 512M
    instances: 1
    buildpacks:
      - python_buildpack
    command: gunicorn app:app -b 0.0.0.0:$PORT
    env:
      PIP_NO_INDEX: false
      PIP_FIND_LINKS: vendor/
```

---

### **3. Deploy to PCF**
Now, push your app again:

```sh
cf push my-python-api
```

---

### **4. Debugging Proxy Issues**
If installation still fails:
1. **Check Logs**:  
   ```sh
   cf logs my-python-api --recent
   ```
2. **Check Proxy Settings in PCF**:  
   ```sh
   cf env my-python-api
   ```
3. **Verify Network Connectivity Inside PCF Shell**:  
   ```sh
   cf ssh my-python-api
   curl https://pypi.org
   ```

---

### **Summary**
✅ **Approach 1**: Use `HTTP_PROXY` & `HTTPS_PROXY` in `manifest.yml`.  
✅ **Approach 2**: Pre-download dependencies (`pip download`) and package them inside your app.  

Let me know if you need further troubleshooting! 🚀
