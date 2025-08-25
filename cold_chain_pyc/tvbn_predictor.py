# -*- coding: utf-8 -*-
"""
tvbn_predictor.py
封装 TVBN 模型的加载和预测逻辑。
"""

import os
import numpy as np
import joblib

from advanced_prediction_models import build_poly_models


class TVBNPredictor:
    def __init__(self, model_path="tvbn_predictor_model.pkl"):
        """
        初始化预测器，加载训练好的模型。
        :param model_path: 模型文件路径
        """
        abs_path = os.path.join(os.path.dirname(__file__), model_path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"❌ 模型文件未找到: {abs_path}")
        self.model = joblib.load(abs_path)
        self.poly_models_cache = {}

        print(f"✅ 模型已成功加载: {abs_path}")

    def make_features(self, time_h, temp_c):
        """
        根据时间和温度构建特征。
        """
        return np.array([[time_h,
                          np.log1p(time_h),
                          temp_c,
                          temp_c ** 2,
                          time_h * temp_c]])

    def predict(self, time_h, temp_c):
        """
        预测 TVBN 含量 (mg/100g)。
        """
        features = self.make_features(time_h, temp_c)
        return float(self.model.predict(features)[0])


    def get_poly_models(self, temps, time_max=2000, poly_order=3):
        """
        获取或构建多项式拟合曲线，避免重复计算。
        """
        key = (tuple(sorted(temps)), time_max, poly_order)
        if key not in self.poly_models_cache:
            print(f"⚡ 缓存未命中，重新构建多项式曲线：temps={temps}")
            self.poly_models_cache[key] = build_poly_models(self.model, temps, time_max, poly_order)
        else:
            print(f"⚡ 缓存已命中，调用temps多项式曲线")
        return self.poly_models_cache[key]