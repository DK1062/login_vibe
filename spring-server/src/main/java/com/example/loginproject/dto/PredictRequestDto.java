package com.example.loginproject.dto;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;

public record PredictRequestDto(
        @NotNull(message = "키를 입력해주세요.")
        @DecimalMin(value = "100.0", message = "키는 100cm 이상 입력해주세요.")
        @DecimalMax(value = "250.0", message = "키는 250cm 이하로 입력해주세요.")
        Double height,

        @NotNull(message = "몸무게를 입력해주세요.")
        @DecimalMin(value = "25.0", message = "몸무게는 25kg 이상 입력해주세요.")
        @DecimalMax(value = "250.0", message = "몸무게는 250kg 이하로 입력해주세요.")
        Double weight
) {
}
