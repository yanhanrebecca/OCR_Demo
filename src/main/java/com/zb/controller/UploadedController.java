package com.zb.controller;

import com.zb.Result.ResultBuilder;
import com.zb.entity.Casefile;
import com.zb.entity.Cases;
import com.zb.entity.Uploaded;
import com.zb.service.*;
import com.zb.tools.*;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @auther 宋亚涛
 * @verson 1.0
 */
@RestController
@RequestMapping("/uploaded")
@CrossOrigin//解决跨域问题
@Slf4j
public class UploadedController {
    @Autowired
    private UploadedService uploadedService;

    @Autowired
    CasefileService casefileService;
    @Autowired
    private CropService cropService;
    @Autowired
    private TwoService twoService;
    @Autowired
    private ThreeService threeService;
    @Autowired
    private FourService fourService;
    @Autowired
    private ColorService colorService;
    @Autowired
    private HistogramService histogramService;
    @Autowired
    private MatchService matchService;
    @Autowired
    private StrokeService strokeService;

    private Map<Integer, Integer> uploadCounts = new HashMap<>();
    private CropTool cropTool = null;
    String newFileName = null;


    //上传图片，保存原图，剪裁文件名，剪裁结果到数据库ok
    //注意：上传的两张图片不能重名
    /*

            返回了caseId 和 case_file_id 前端可以从这里获取
            list.add(uploadedId);
            list.add(case_file_id);
     */
    @ApiOperation("上传图片的接口")
    @PostMapping("/{caseId}/add")
    public HttpResponse<List<Integer>> addPictureAndFileNameAndResult(@PathVariable("caseId") int caseId, @RequestParam("image") MultipartFile file) {

        //如果已经上传并且已经生成结果就删除重新上传生成
        //如果已经上传了一张图片数据库中原始图片有一张，别的库中没有
        //本地文件夹中有原始图片和结果
        //首先根据caseId查casefile,如果不为空，就全部删除，如果为空，说明只上传了一张不删除
        //这个就完成了类似更新的操作

        List<Casefile> caseFiles = casefileService.getAll(caseId);
        String flag;

        if (!(caseFiles == null || caseFiles.isEmpty())) {
            delete(caseId);
        }

        BufferedReader in = null;

        Integer uploadedId = null;
        Integer case_file_id = null;
        List<Integer> list = new ArrayList<>();


        if (file.isEmpty()) { // 上传的图片文件为空
            return ResultBuilder.faile(ResultCode.USER_NULL_PICTURE_ERROR);
        }
        if(uploadCounts.get(caseId)==null){
            flag = "";
        }else{
            flag = "";
        }
        String fileName = file.getOriginalFilename();
        int dotIndex1 = fileName.lastIndexOf('.');
        if (dotIndex1 != -1) {
            // 获取文件名部分（不包括扩展名）
            String nameWithoutExtension = fileName.substring(0, dotIndex1);
            // 获取扩展名部分
            String extension = fileName.substring(dotIndex1);

            // 新的文件名，在文件名后添加 "_jc"
            String newFileName = nameWithoutExtension + flag + extension;

            System.out.println(newFileName);
            fileName = newFileName;
        } else {
            System.out.println("文件名没有找到扩展名。");
        }
        String file_path = AppRootPath.getappRootPath_ori() + fileName;
        File destinationFile = new File(file_path);

        try {
            file.transferTo(destinationFile); // 保存上传的图片到本地
            //保存上传的图片到数据库
            uploadedService.createUpload(caseId, file_path);
            CallPad_test.Call(fileName, in, caseId);//调用python程序,剪裁后的图片保存到相应案件的文件夹中

            // 增加上传计数
            uploadCounts.put(caseId, uploadCounts.getOrDefault(caseId, 0) + 1);
            System.out.println(uploadCounts.get(caseId) + "===========================");

            if (uploadCounts.get(caseId) == 2) {
                int dotIndex = fileName.lastIndexOf('.');
                if (dotIndex > 0) {
                    newFileName = fileName.substring(0, dotIndex);
                }
                uploadedId = uploadedService.findIdByCaseIdAndName(caseId, newFileName);

                //把结果的文件夹名字以及地址保存到数据库
                String directoryPath = AppRootPath.getappRootPath_result() + caseId + "\\picture";
                File directory = new File(directoryPath);
                if (directory.isDirectory()) {
                    File[] subfolders = directory.listFiles(File::isDirectory);
                    if (subfolders != null) {
                        for (File subfolder : subfolders) {
                            String folderName = subfolder.getName();
                            String folderPath = subfolder.getAbsolutePath();

                            case_file_id = casefileService.insert(folderName, folderPath, caseId, uploadedId);//文件名，文件路径入库
                            list.add(case_file_id);
                        }
                    }
                } else {
                    System.out.println("Provided path is not a directory.");
                }
                // 进行图片裁剪
                cropTool = new CropTool();
                cropTool.CropToDB(fileName, caseId, uploadedService, cropService, casefileService);
                list.add(uploadedId);//第二张图片的 uploadedId
                // 重置计数
                uploadCounts.put(caseId, 0);
            }

        } catch (Exception e) {
            e.printStackTrace();
            return ResultBuilder.faile(ResultCode.CODE_ERROR);

        } finally {
            if (in != null) {
                try {
                    in.close();
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        }
        return ResultBuilder.success(list, ResultCode.SAVE_SUCCESS);
    }

    @ApiOperation("删除本案件中的东西")
    @DeleteMapping("/delete/{caseId}")//ok
    public HttpResponse delete(@PathVariable Integer caseId) {

        //删除ori文件夹下的相应文件
        List<String> imagePaths = uploadedService.findPathByCaseId(caseId);
        for (String imagePath : imagePaths) {
            try {
                Path path = Paths.get(imagePath);
                // 删除文件
                Files.deleteIfExists(path);
                System.out.println("Deleted: " + imagePath);
            } catch (IOException e) {
                System.err.println("Failed to delete " + imagePath + ": " + e.getMessage());
            }
        }
        //删除uploaded数据库,一次删除两个
        uploadedService.deleteByCaseId(caseId);//ok
        //根据uploadedId删除casefile数据库
        casefileService.deleteByCaseId(caseId);
        //根据uploadedId删除crop数据库
        cropService.deleteByCaseId(caseId);

        //删除color数据库
        colorService.deleteByCaseId(caseId);
        //删除his数据库
        histogramService.deleteByCaseId(caseId);
        //删除two数据库
        twoService.deleteByCaseId(caseId);
        //删除three数据库
        threeService.deleteByCaseId(caseId);
        //删除four数据库
        fourService.deleteByCaseId(caseId);
        //删除Stroke数据库
        strokeService.deleteByCaseId(caseId);
        //删除match数据库
        matchService.deleteByCaseId(caseId);

        //删除caseId文件夹下的所有文件
        Path directory1 = Paths.get(AppRootPath.getappRootPath_result() + caseId);
        try {
            // 检查目录是否存在
            if (Files.exists(directory1) && Files.isDirectory(directory1)) {
                // 列出文件夹中的所有文件和子目录并删除
                Files.list(directory1).forEach(path -> {
                    try {
                        if (Files.isDirectory(path)) {
                            DeleteTools.deleteContents(path); // 递归删除子目录
                        }
                        Files.delete(path); // 删除文件
                    } catch (IOException e) {
                        System.err.println("删除失败: " + path + " " + e.getMessage());
                    }
                });
                System.out.println("所有文件已删除，文件夹1保留。");
            } else {
                System.out.println("目录不存在: " + directory1);
            }
        } catch (IOException e) {
            System.err.println("读取文件夹失败: " + e.getMessage());
        }

        return ResultBuilder.successNoData(ResultCode.DELETE_SUCCESS);


    }

    //加载数据ok
    @RequestMapping("/load")
    public HttpResponse<Uploaded> load(Integer id) {
        return ResultBuilder.success(uploadedService.getById(id), ResultCode.QUERY_SUCCESS);
    }
}
