package com.zb.controller;

import com.zb.Result.ResultBuilder;
import com.zb.service.CasefileService;
import com.zb.service.ThreeService;
import com.zb.service.UploadedService;
import com.zb.tools.*;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

/**
 * @auther 宋亚涛
 * @verson 1.0
 */
@RestController
@RequestMapping("/three")
@CrossOrigin//解决跨域问题
@Slf4j
public class ThreeController {
    @Autowired
    private ThreeService threeService;
    @Autowired
    private UploadedService uploadedService;
    @Autowired
    private CasefileService casefileService;


    //对识别成功的结果进行三维处理，增
    @ApiOperation("对识别成功的结果进行三维处理，增")
    @PostMapping("/add/{caseId}")
    public HttpResponse threeDimensional(@PathVariable("caseId") int caseId) {

        List<?> threeFiles = threeService.getAll(caseId);
        if (threeFiles == null || threeFiles.isEmpty()) {
            BufferedReader in = null;

            //调用 Three_Dimensional_recognition.py
            try {
                CallThree.Call(in, caseId);
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

            //将三维结果保存到数据库
            return DimensionTools.toDB(caseId, uploadedService, threeService, casefileService, "three_dimensional");
        } else {
            System.out.println("已经存在，不重复添加");
            return ResultBuilder.successNoData(ResultCode.SAVE_SUCCESS);
        }

    }

    //查

    @ApiOperation("将3维结果返回给前端，查")
    @RequestMapping("/load/{caseId}/{case_file_id}")
    public HttpResponse<List<String>> createFileNameButton(@PathVariable("caseId") int caseId,
                                                           @PathVariable("case_file_id") int id) {
        List<String> imageUrls = threeService.getCropsByCaseIdAndFileId(caseId, id);
        String baseUrl = "http://localhost:8080/";
        List<String> updatedPaths = imageUrls.stream()
                .map(path -> path.replace(AppRootPath.getappRootPath_static(), baseUrl)
                        .replace("\\", "/"))
                .collect(Collectors.toList());
        System.out.println(updatedPaths);
        return ResultBuilder.success(updatedPaths, ResultCode.QUERY_SUCCESS);
    }
}
