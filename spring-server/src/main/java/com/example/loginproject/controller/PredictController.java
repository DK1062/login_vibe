package com.example.loginproject.controller;

import com.example.loginproject.dto.PredictRequestDto;
import com.example.loginproject.dto.PredictResponseDto;
import com.example.loginproject.service.PredictService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
@RequiredArgsConstructor
public class PredictController {

    private final PredictService predictService;

    @GetMapping("/predict")
    public String predictForm(Model model) {
        model.addAttribute("predictRequestDto", new PredictRequestDto(null, null));
        return "predict/form";
    }

    @PostMapping("/predict")
    public String predict(
            @Valid @ModelAttribute PredictRequestDto request,
            BindingResult bindingResult,
            Model model
    ) {
        if (bindingResult.hasErrors()) {
            return "predict/form";
        }

        try {
            PredictResponseDto response = predictService.predict(request);
            model.addAttribute("request", request);
            model.addAttribute("response", response);
            return "predict/result";
        } catch (IllegalStateException e) {
            bindingResult.reject("predictError", e.getMessage());
            return "predict/form";
        }
    }
}
