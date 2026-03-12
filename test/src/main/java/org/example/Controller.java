package org.example;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
public class Controller {

    @Autowired
    private MathService mathService;

    @GetMapping("/api/hello")
    public Map<String, String> getHello() {
        Map<String, String> response = new HashMap<>();
        response.put("message", "hello world");
        return response;
    }

    @GetMapping("/api/hello/{name}")
    public Map<String, String> getHelloWithName(@PathVariable String name) {
        Map<String, String> response = new HashMap<>();
        response.put("message", name);
        return response;
    }

    @GetMapping("/api/math/{a}/{b}")
    public Map<String, String> getMath(@PathVariable int a, @PathVariable int b) {
        Map<String, String> response = new HashMap<>();
        response.put("sum", String.valueOf(mathService.add(a, b)));
        response.put("multiplication", String.valueOf(mathService.multiply(a, b)));
        return response;
    }

    @PostMapping("/api/math/")
    public Map<String, String> doMathPost(@RequestBody Map<String, Integer> request) {
        int a = request.get("a");
        int b = request.get("b");
        Map<String, String> response = new HashMap<>();
        response.put("sum", String.valueOf(mathService.add(a, b)));
        response.put("multiplication", String.valueOf(mathService.multiply(a, b)));
        return response;
    }

}
