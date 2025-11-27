from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl
import tempfile,os,sys,warnings
from typing_extensions import override
MOD_MAP_EDIT_MOD = os.getenv("MOD_MAP_EDIT_MOD")
MOD_MAP_DEV = "mod_dev"

if MOD_MAP_EDIT_MOD == MOD_MAP_DEV:
    warnings.filterwarnings("ignore", 
                        message=".*sipPyTypeDict.*is deprecated.*")
    warnings.filterwarnings("ignore",
                        message=".*sipPyTypeDict.*deprecated.*sipPyTypeDictRef.*")
    warnings.filterwarnings("ignore", message=".*GPS.*")


class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super(CustomWebEnginePage, self).__init__(parent)
        # print("CustomWebEnginePage initialized")  
        
        # 连接权限请求信号
        self.featurePermissionRequested.connect(self.handleFeaturePermissionRequested)
    
    @override
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        """处理JavaScript控制台消息"""
        if MOD_MAP_EDIT_MOD == MOD_MAP_DEV:
            level_str = {0: "INFO", 1: "WARNING", 2: "ERROR"}.get(level, "UNKNOWN")
            print(f"JS {level_str} [Line {lineNumber}]: {message}")
            pass
    
    def handleFeaturePermissionRequested(self, securityOrigin, feature):
        """处理功能权限请求"""
        # print(f"权限请求: 来源={securityOrigin.host()}, 功能={feature}")
        
        # 检查是否为位置权限请求
        if feature == QWebEnginePage.Geolocation:
            # print("位置权限请求处理")
            # test：统一同意定位请求
            self.setFeaturePermission(securityOrigin, feature, QWebEnginePage.PermissionGrantedByUser)
            
            return 
            # 弹出对话框询问用户 - 修复参数类型
            reply = QMessageBox.question(
                self.view(),
                "位置权限请求",
                f"网站 {securityOrigin.host()} 请求获取您的位置信息。是否允许？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No  # 使用正确的 QMessageBox 标准按钮
            )
            
            if reply == QMessageBox.Yes:
                # 授予权限
                self.setFeaturePermission(securityOrigin, feature, QWebEnginePage.PermissionGrantedByUser)
                print("位置权限已授予")
            else:
                # 拒绝权限
                self.setFeaturePermission(securityOrigin, feature, QWebEnginePage.PermissionDeniedByUser)
                print("位置权限已拒绝")
        else:
            # 对于其他权限请求，默认拒绝
            self.setFeaturePermission(securityOrigin, feature, QWebEnginePage.PermissionDeniedByUser)
            print(f"权限已拒绝: {feature}")

class RealTimeMapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('高德地图路径规划与定位')
        self.resize(1000, 700)
        
        # 创建临时HTML文件
        self.temp_file = self.create_temp_html()
        
        self.init_ui()
    
        # 连接加载完成信号
        self.web_view.loadFinished.connect(self.on_map_loaded)
    
    def create_temp_html(self):
        """创建临时HTML文件"""
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, "amap_demo.html")
        
        # 读取HTML文件内容
        try:
            with open("./controller/realTimeMapSrc.html", "r", encoding='utf-8') as f:
                map_src = f.read()
            with open(temp_file_path, 'w', encoding='utf-8') as f:
                f.write(map_src)
            # print(f"临时HTML文件已创建: {temp_file_path}")
            return temp_file_path
        except Exception as e:
            print(f"创建临时文件失败: {e}")
            # 使用备用方案
            return None
    
    def init_ui(self):
        """初始化UI"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建WebEngineView
        self.web_view = QWebEngineView()
        
        # 创建自定义页面
        self.web_page = CustomWebEnginePage(self.web_view)
        self.web_view.setPage(self.web_page)

        self.qwebengine = self.web_view

        # 配置WebEngine设置以支持地理位置
        self.configure_web_settings()
        
        # 添加到布局
        layout.addWidget(self.web_view)
        
        # 添加状态栏信息
        self.statusBar().showMessage("地图加载中...")
    
    def configure_web_settings(self):
        """配置WebEngine设置"""
        settings = self.web_view.settings()
        

        # # 启用JavaScript
        settings.setAttribute(settings.JavascriptEnabled, True)
        
        # 启用本地存储
        settings.setAttribute(settings.LocalStorageEnabled, True)
        
        
        # print("WebEngine设置已配置")
    
    def load_map(self):
        """加载地图"""
        if self.temp_file and os.path.exists(self.temp_file):
            # 加载临时HTML文件
            url = QUrl.fromLocalFile(self.temp_file)
            self.web_view.load(url)
            # print("从临时文件加载地图")
        else:
            # 读取HTML内容作为备用方案
            try:
                with open("./controller/realTimeMapSrc.html", "r", encoding='utf-8') as f:
                    map_src = f.read()
                self.web_view.setHtml(map_src)
                print("直接设置HTML内容")
            except Exception as e:
                print(f"加载地图失败: {e}")
        
        
    def on_map_loaded(self, success):
        """地图加载完成回调"""
        if success:
            self.statusBar().showMessage("地图加载完成")
            # print("地图加载完成")
            
            # 注入JavaScript代码以增强功能
            self.inject_enhancement_script()
        else:
            self.statusBar().showMessage("地图加载失败")
            # print("地图加载失败")
    
    def inject_enhancement_script(self):
        if(MOD_MAP_EDIT_MOD!=MOD_MAP_DEV):return
        """注入增强功能的JavaScript代码"""
        enhancement_script = """
        // 增强功能：添加更详细的错误处理和状态反馈
        window.addEventListener('error', function(e) {
            console.error('全局错误:', e.error);
        });
        
        // 监听地理位置权限变化
        if (navigator.permissions) {
            navigator.permissions.query({name: 'geolocation'}).then(function(permissionStatus) {
                permissionStatus.onchange = function() {
                    console.log('地理位置权限状态变化:', this.state);
                };
            });
        }
        
        // 添加自定义事件监听器
        document.addEventListener('amapReady', function() {
            console.log('高德地图已准备就绪');
        });
        """
        
        # 执行JavaScript代码
        self.web_view.page().runJavaScript(enhancement_script)
        print("增强功能脚本已注入")

    def closeEvent(self, event):
        """应用程序关闭事件"""
        print("close====")
        # 清理临时文件
        if hasattr(self, 'temp_file') and self.temp_file and os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
                print("临时map文件已清理")
            except Exception as e:
                print(f"清理map临时文件失败: {e}")
        
        event.accept()
    def refresh(self):
        self.load_map()
        pass
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    
    # 设置应用程序信息
    app.setApplicationName("高德地图路径规划")
    app.setApplicationVersion("1.0")
    
    # 创建并显示主窗口
    window = RealTimeMapApp()
    window.show()
    
    sys.exit(app.exec_())