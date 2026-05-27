package com.example.loginproject.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record MemberSignupRequest(
        @NotBlank(message = "아이디를 입력해주세요.")
        @Size(min = 4, max = 50, message = "아이디는 4자 이상 50자 이하로 입력해주세요.")
        String username,

        @NotBlank(message = "비밀번호를 입력해주세요.")
        @Size(min = 4, max = 100, message = "비밀번호는 4자 이상 입력해주세요.")
        String password,

        @NotBlank(message = "이름을 입력해주세요.")
        @Size(max = 50, message = "이름은 50자 이하로 입력해주세요.")
        String name
) {
}
