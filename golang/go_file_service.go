package main

import (
    "errors"
    "fmt"
    "net"
    "net/http"
    "os"
    "os/exec"
    "path/filepath"
    "strconv"
    "time"
)

func main(){
    port := getPort()
    go checkPort(port)
    //time.Sleep(time.Millisecond)
    startHttp(port)
}

func getPort() string {
    port := ""
    isPortValid := false
    for isPortValid == false {
        fmt.Print("请输入共享端口号(小于65535的正整数, 比如80): ")
        fmt.Scanln(&port)
        if len(port) == 0 {
            continue
        } else {
            portNum, err := strconv.ParseInt(port, 10, 64)
            if err != nil || portNum > 65535 || portNum < 0 {
                port = ""
                fmt.Println("端口号需为小于65535的正整数")
            } else {
                isPortValid = true
            }
        }
    }
    return port
}

func checkPort(port string) {
    fmt.Println("服务(" + port + ")启动中...")
    for {
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
    ip, err := getActualIP()
    if err != nil {
        fmt.Println(err)
    } else {
        showRemind(ip.String(), port)
    }
}

func startHttp(port string) {
    p, _ := filepath.Abs(filepath.Dir(os.Args[0]))
    http.Handle("/", http.FileServer(http.Dir(p)))
    err := http.ListenAndServe(":"+port, nil)
    if err != nil {
        fmt.Println(err)
    }
}

func showRemind(ip, port string) {
    url := "http://" + ip + ":" + port
    fmt.Println("请在浏览器打开 " + url + " 来访问共享文件")
    fmt.Println("共享目录为本程序所在目录")
    fmt.Println("直接关掉本窗口即可停止共享")
    time.Sleep(time.Second)
    cmd := exec.Command("explorer", url)
    cmd.Start()
}

func getActualIP() (net.IP, error) {
    ifaces, err := net.Interfaces()
    if err != nil {
        return nil, err
    }
    for _, iface := range ifaces {
        if iface.Flags & net.FlagUp == 0 {
            continue // interface down
        }
        if iface.Flags & net.FlagLoopback != 0 {
            continue // loopback interface
        }
        addrs, err := iface.Addrs()
        if err != nil {
            return nil, err
        }
        for _, addr := range addrs {
            ip := getIpFromAddr(addr)
            if ip == nil {
                continue
            }
            return ip, nil
        }
    }
    return nil, errors.New("connected to the network?")
}

func getIpFromAddr(addr net.Addr) net.IP {
    var ip net.IP
    switch v := addr.(type) {
    case *net.IPNet:
        ip = v.IP
    case *net.IPAddr:
        ip = v.IP
    }
    if ip == nil || ip.IsLoopback() {
        return nil
    }
    ip = ip.To4()
    if ip == nil {
        return nil // not an ipv4 address
    }
    return ip
}
