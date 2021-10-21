package main

import (
    "fmt"
    "net"
    "net/http"
    "os"
    "path/filepath"
    "strconv"
    "strings"
    "time"
)

func main(){
    port := GetPort()
    go CheckPort(port)
    StartHttp(port)
}

func GetPort() string {
    var port string
    is_num := false
    for is_num == false {
        fmt.Print("请输入共享端口号(纯数字, 比如80): ")
        fmt.Scanln(&port)
        if len(port) == 0 {
            continue
        } else {
            is_num = IsNum(port)
            if is_num == false {
                port = ""
                fmt.Println("端口号需为纯数字")
            }
        }
    }
    return port
}

func CheckPort(port string) {
    fmt.Println("服务(" + port + ")启动中...")
    for {
        time.Sleep(time.Millisecond)
        resp, err := http.Get("http://localhost:" + port)
        if err != nil {
            continue
        }
        resp.Body.Close()
        if resp.StatusCode != http.StatusOK {
            continue
        }
        break
    }
    fmt.Println("服务(" + port + ")已启动...")
    DisplayRemind(port)
}

func DisplayRemind(port string) {
    addrs, err := net.InterfaceAddrs()
    if err != nil{
        fmt.Println(err)
        return
    }
    for _, value := range addrs{
        if ipnet, ok := value.(*net.IPNet); ok && !ipnet.IP.IsLoopback(){
            if ipnet.IP.To4() != nil{
                ip := ipnet.IP.String()
                if strings.HasPrefix(ip, "10.204") || strings.HasPrefix(ip, "172.32") || strings.HasPrefix(ip, "192.168.48") {
                    fmt.Println("请在浏览器打开 http://" + ip + ":" + port + " 来访问共享文件")
                    fmt.Println("共享目录为本程序所在目录")
                    fmt.Println("直接关掉本窗口即可停止共享")
                    break
                }
            }
        }
    }
}

func StartHttp(port string){
    p, _ := filepath.Abs(filepath.Dir(os.Args[0]))
    http.Handle("/", http.FileServer(http.Dir(p)))
    err := http.ListenAndServe(":" + port, nil)
    if err != nil {
        fmt.Println(err)
    }
}

func IsNum(s string) bool {
    _, err := strconv.ParseFloat(s, 64)
    return err == nil
}
