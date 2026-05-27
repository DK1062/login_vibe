package com.example.loginproject.controller;

import com.example.loginproject.dto.MemberSignupRequest;
import com.example.loginproject.service.MemberService;
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
public class MemberController {

    private final MemberService memberService;

    @GetMapping("/members/signup")
    public String signupForm(Model model) {
        model.addAttribute("memberSignupRequest", new MemberSignupRequest("", "", ""));
        return "member/signup";
    }

    @PostMapping("/members/signup")
    public String signup(
            @Valid @ModelAttribute MemberSignupRequest request,
            BindingResult bindingResult
    ) {
        if (bindingResult.hasErrors()) {
            return "member/signup";
        }

        try {
            memberService.signup(request);
        } catch (IllegalArgumentException e) {
            bindingResult.reject("signupError", e.getMessage());
            return "member/signup";
        }

        return "redirect:/login";
    }

    @GetMapping("/members")
    public String memberList(Model model) {
        model.addAttribute("members", memberService.findAllMembers());
        return "member/list";
    }
}
