package com.zb.controller;
import com.zb.Result.ResultBuilder;
import com.zb.tools.AppRootPath;
import com.zb.tools.HttpResponse;
import com.zb.tools.ResultCode;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

/**
 * @auther 宋亚涛
 * @verson 1.0
 */
@RestController
@RequestMapping("/fractal")
@CrossOrigin//解决跨域问题
@Slf4j
public class FractalController {
    @ApiOperation("上传图片的接口")
    @PostMapping("/add")
    public HttpResponse<String> addFractal(@RequestParam("image") MultipartFile image) {
        // 指定文件夹路径
        String folderPath = AppRootPath.getappRootPath_images() + "fractal";
        System.out.println(folderPath);
        // 创建文件夹对象
        File folder = new File(folderPath);

        // 检查文件夹是否存在且不为空
        if (folder.exists() && folder.isDirectory()) {
            File[] files = folder.listFiles();

            if (files != null && files.length > 0) {
                // 删除文件夹中的所有文件
                for (File file : files) {
                    if (file.isFile()) {
                        file.delete();
                    }
                }
                System.out.println("Folder cleared successfully.");
            } else {
                System.out.println("Folder is already empty.");
            }
        } else {
            System.out.println("Folder does not exist.");
        }

        //保存图片到本地
        File directory = new File(folderPath);
        if (!directory.exists()) {
            directory.mkdirs(); // 创建文件夹
        }

        File fileToSave = new File(directory, image.getOriginalFilename());
        try {
            image.transferTo(fileToSave); // 保存文件
        } catch (IOException e) {
            e.printStackTrace(); // 处理异常
        }
        StringBuilder output = new StringBuilder();

        try {
            // 指定Python脚本路径和图像路径
            String pythonScriptPath = AppRootPath.getappRootPath_python() + "Fractal.py";
            String imagePath = folderPath + "\\" + image.getOriginalFilename();
            System.out.println(imagePath);

            // 创建ProcessBuilder以调用Python脚本
            ProcessBuilder processBuilder = new ProcessBuilder(
                    "python", pythonScriptPath, imagePath);

            // 启动进程
            Process process = processBuilder.start();

            // 读取Python脚本的标准输出
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;

            while ((line = reader.readLine()) != null) {
                output.append(line);
            }

            // 等待脚本执行完毕
            process.waitFor();

            // 输出分形维数
            System.out.println("Fractal Dimension: " + output.toString().trim());

        } catch (Exception e) {
            e.printStackTrace();
        }
        return ResultBuilder.success(output.toString().trim(), ResultCode.SAVE_SUCCESS);
    }
}