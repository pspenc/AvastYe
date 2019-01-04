// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "AvastYeCppBPFuncLibrary.generated.h"

/**
 * 
 */
UCLASS()
class AVASTYE_API UAvastYeCppBPFuncLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
public:

	UFUNCTION(BlueprintCallable, meta = (DisplayName = "Get Child Classes", Keywords = "Get Child Classes"), Category = Class)
		static TArray<UClass*> GetClasses(UClass* ParentClass);
};
