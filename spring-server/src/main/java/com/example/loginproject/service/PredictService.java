package com.example.loginproject.service;

import com.example.loginproject.dto.PredictRequestDto;
import com.example.loginproject.dto.PredictResponseDto;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

@Service
@RequiredArgsConstructor
public class PredictService {

    private final RestTemplate restTemplate;

    @Value("${flask.predict-url:http://localhost:5000/predict}")
    private String predictUrl;

    public PredictResponseDto predict(PredictRequestDto request) {
        try {
            PredictResponseDto response = restTemplate.postForObject(
                    predictUrl,
                    request,
                    PredictResponseDto.class
            );

            if (response == null || response.result() == null || response.result().isBlank()) {
                throw new IllegalStateException("Flask 서버에서 예측 결과를 받지 못했습니다.");
            }

            return response;
        } catch (RestClientException e) {
            throw new IllegalStateException("Flask 예측 서버와 통신할 수 없습니다.", e);
        }
    }
}
