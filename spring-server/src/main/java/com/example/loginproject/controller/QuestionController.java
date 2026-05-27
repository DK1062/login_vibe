package com.example.loginproject.controller;

import com.example.loginproject.dto.QuestionCreateRequest;
import com.example.loginproject.dto.QuestionResponse;
import com.example.loginproject.dto.QuestionUpdateRequest;
import com.example.loginproject.service.QuestionService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequiredArgsConstructor
public class QuestionController {

    private final QuestionService questionService;

    @GetMapping("/questions")
    public String list(Model model) {
        model.addAttribute("questions", questionService.findAll());
        return "question/list";
    }

    @GetMapping("/questions/{id}")
    public String detail(@PathVariable Long id, Authentication authentication, Model model) {
        QuestionResponse question = questionService.findById(id);
        model.addAttribute("question", question);
        model.addAttribute("canModify", questionService.canModify(id, authentication));
        return "question/detail";
    }

    @GetMapping("/questions/new")
    public String createForm(Model model) {
        model.addAttribute("questionCreateRequest", new QuestionCreateRequest("", ""));
        return "question/form";
    }

    @PostMapping("/questions")
    public String create(
            @Valid @ModelAttribute QuestionCreateRequest request,
            BindingResult bindingResult,
            Authentication authentication
    ) {
        if (bindingResult.hasErrors()) {
            return "question/form";
        }

        Long questionId = questionService.create(request, authentication.getName());
        return "redirect:/questions/" + questionId;
    }

    @GetMapping("/questions/{id}/edit")
    public String updateForm(
            @PathVariable Long id,
            Authentication authentication,
            Model model,
            RedirectAttributes redirectAttributes
    ) {
        try {
            model.addAttribute("questionId", id);
            model.addAttribute("questionUpdateRequest", questionService.findUpdateForm(id, authentication));
            return "question/edit";
        } catch (IllegalStateException e) {
            redirectAttributes.addFlashAttribute("errorMessage", e.getMessage());
            return "redirect:/questions/" + id;
        }
    }

    @PostMapping("/questions/{id}/edit")
    public String update(
            @PathVariable Long id,
            @Valid @ModelAttribute QuestionUpdateRequest request,
            BindingResult bindingResult,
            Authentication authentication,
            Model model,
            RedirectAttributes redirectAttributes
    ) {
        if (bindingResult.hasErrors()) {
            model.addAttribute("questionId", id);
            return "question/edit";
        }

        try {
            questionService.update(id, request, authentication);
        } catch (IllegalStateException e) {
            redirectAttributes.addFlashAttribute("errorMessage", e.getMessage());
            return "redirect:/questions/" + id;
        }

        return "redirect:/questions/" + id;
    }

    @PostMapping("/questions/{id}/delete")
    public String delete(
            @PathVariable Long id,
            Authentication authentication,
            RedirectAttributes redirectAttributes
    ) {
        try {
            questionService.delete(id, authentication);
        } catch (IllegalStateException e) {
            redirectAttributes.addFlashAttribute("errorMessage", e.getMessage());
            return "redirect:/questions/" + id;
        }

        return "redirect:/questions";
    }
}
